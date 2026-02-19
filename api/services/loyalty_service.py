"""
Forkast Loyalty Service
Tier-based loyalty program for restaurant-supplier relationships.
Restaurants earn tiers based on 90-day rolling order count with each supplier.
Higher tiers reduce the Forkast platform fee (discount absorbed by Forkast).
"""
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.db_models import (
    LoyaltyAccountDB, LoyaltyTransactionDB, PaymentDB, SupplierDB,
)

# Tier definitions - ordered from lowest to highest
TIERS = [
    {"name": "standard",  "min_orders": 0,   "discount": 0.0, "fee": 15.0},
    {"name": "bronze",    "min_orders": 25,  "discount": 2.0, "fee": 13.0},
    {"name": "silver",    "min_orders": 50,  "discount": 3.0, "fee": 12.0},
    {"name": "gold",      "min_orders": 100, "discount": 5.0, "fee": 10.0},
    {"name": "platinum",  "min_orders": 200, "discount": 7.0, "fee": 8.0},
]


def _tier_for_orders(order_count: int) -> dict:
    """Determine tier based on order count."""
    result = TIERS[0]
    for tier in TIERS:
        if order_count >= tier["min_orders"]:
            result = tier
    return result


def _next_tier(current_tier_name: str) -> Optional[dict]:
    """Get the next tier above current, or None if at max."""
    for i, tier in enumerate(TIERS):
        if tier["name"] == current_tier_name:
            if i + 1 < len(TIERS):
                return TIERS[i + 1]
            return None
    return None


class LoyaltyService:
    """Loyalty program business logic."""

    @staticmethod
    def get_tier_definitions() -> list:
        """Return all tier definitions."""
        return TIERS

    @staticmethod
    def count_recent_orders(
        db: Session, restaurant_uid: str, supplier_uid: str, days: int = 90
    ) -> int:
        """Count succeeded payments in the rolling window."""
        cutoff = datetime.now() - timedelta(days=days)
        return db.query(PaymentDB).filter(
            PaymentDB.restaurant_uid == restaurant_uid,
            PaymentDB.supplier_uid == supplier_uid,
            PaymentDB.status == "succeeded",
            PaymentDB.created_at >= cutoff,
        ).count()

    @staticmethod
    def get_or_create_account(
        db: Session, restaurant_uid: str, supplier_uid: str
    ) -> LoyaltyAccountDB:
        """Get existing loyalty account or create a new one."""
        account = db.query(LoyaltyAccountDB).filter(
            LoyaltyAccountDB.restaurant_uid == restaurant_uid,
            LoyaltyAccountDB.supplier_uid == supplier_uid,
        ).first()

        if not account:
            account = LoyaltyAccountDB(
                restaurant_uid=restaurant_uid,
                supplier_uid=supplier_uid,
                current_tier="standard",
                orders_90d=0,
                total_orders=0,
                total_spent=0.0,
                discount_pct=0.0,
                effective_fee=15.0,
            )
            db.add(account)
            db.commit()
            db.refresh(account)

        return account

    @staticmethod
    def evaluate_tier(db: Session, account: LoyaltyAccountDB) -> bool:
        """Re-evaluate tier based on 90-day rolling window. Returns True if tier changed."""
        orders_90d = LoyaltyService.count_recent_orders(
            db, account.restaurant_uid, account.supplier_uid
        )
        new_tier_info = _tier_for_orders(orders_90d)
        old_tier = account.current_tier
        tier_changed = old_tier != new_tier_info["name"]

        account.orders_90d = orders_90d
        account.current_tier = new_tier_info["name"]
        account.discount_pct = new_tier_info["discount"]
        account.effective_fee = new_tier_info["fee"]
        account.last_evaluated = datetime.now()
        account.updated_at = datetime.now()

        if tier_changed:
            event_type = "tier_upgrade" if new_tier_info["fee"] < _tier_for_orders(0)["fee"] and \
                new_tier_info["min_orders"] > _tier_for_orders(
                    sum(1 for t in TIERS if t["name"] == old_tier) * 25
                )["min_orders"] else "tier_downgrade"
            # Simpler: compare positions
            old_idx = next((i for i, t in enumerate(TIERS) if t["name"] == old_tier), 0)
            new_idx = next((i for i, t in enumerate(TIERS) if t["name"] == new_tier_info["name"]), 0)
            event_type = "tier_upgrade" if new_idx > old_idx else "tier_downgrade"

            tx = LoyaltyTransactionDB(
                account_uid=account.uid,
                event_type=event_type,
                order_count=orders_90d,
                old_tier=old_tier,
                new_tier=new_tier_info["name"],
                note=f"Tier changed: {old_tier} -> {new_tier_info['name']} ({orders_90d} orders in 90d)",
            )
            db.add(tx)

        db.commit()
        db.refresh(account)
        return tier_changed

    @staticmethod
    def record_payment(
        db: Session, restaurant_uid: str, supplier_uid: str,
        payment_uid: str, supplier_amount: float, discount_applied: float = 0.0
    ):
        """Record a successful payment and update loyalty account."""
        account = LoyaltyService.get_or_create_account(db, restaurant_uid, supplier_uid)

        account.total_orders += 1
        account.total_spent += supplier_amount

        # Log the payment event
        tx = LoyaltyTransactionDB(
            account_uid=account.uid,
            event_type="payment_completed",
            payment_uid=payment_uid,
            order_count=account.orders_90d + 1,  # Will be updated by evaluate
            old_tier=account.current_tier,
            new_tier=account.current_tier,  # Updated if tier changes
            amount=supplier_amount,
            discount_applied=discount_applied,
            note=f"Payment {payment_uid}: AED {supplier_amount:.2f}",
        )
        db.add(tx)
        db.commit()

        # Re-evaluate tier (may add tier change transaction)
        LoyaltyService.evaluate_tier(db, account)

        # Update the payment transaction with final tier
        tx.new_tier = account.current_tier
        tx.order_count = account.orders_90d
        db.commit()

    @staticmethod
    def get_effective_fee(
        db: Session, restaurant_uid: str, supplier_uid: Optional[str]
    ) -> float:
        """Get the effective Forkast fee % for a restaurant-supplier pair."""
        if not supplier_uid:
            return 15.0

        account = db.query(LoyaltyAccountDB).filter(
            LoyaltyAccountDB.restaurant_uid == restaurant_uid,
            LoyaltyAccountDB.supplier_uid == supplier_uid,
        ).first()

        if account:
            # Re-evaluate to ensure freshness
            LoyaltyService.evaluate_tier(db, account)
            return account.effective_fee

        return 15.0  # Default for new relationships

    @staticmethod
    def get_accounts(
        db: Session, restaurant_uid: str
    ) -> List[LoyaltyAccountDB]:
        """Get all loyalty accounts for a restaurant with supplier names."""
        return db.query(LoyaltyAccountDB).filter(
            LoyaltyAccountDB.restaurant_uid == restaurant_uid,
        ).order_by(LoyaltyAccountDB.current_tier.desc()).all()

    @staticmethod
    def get_account(
        db: Session, restaurant_uid: str, supplier_uid: str
    ) -> Optional[LoyaltyAccountDB]:
        """Get a specific loyalty account."""
        return db.query(LoyaltyAccountDB).filter(
            LoyaltyAccountDB.restaurant_uid == restaurant_uid,
            LoyaltyAccountDB.supplier_uid == supplier_uid,
        ).first()

    @staticmethod
    def get_account_history(
        db: Session, account_uid: str, limit: int = 100
    ) -> List[LoyaltyTransactionDB]:
        """Get transaction history for a loyalty account."""
        return db.query(LoyaltyTransactionDB).filter(
            LoyaltyTransactionDB.account_uid == account_uid,
        ).order_by(LoyaltyTransactionDB.created_at.desc()).limit(limit).all()

    @staticmethod
    def evaluate_all_accounts(db: Session) -> dict:
        """Re-evaluate all loyalty accounts. Returns summary of changes."""
        accounts = db.query(LoyaltyAccountDB).all()
        upgrades = 0
        downgrades = 0
        unchanged = 0

        for account in accounts:
            old_tier = account.current_tier
            LoyaltyService.evaluate_tier(db, account)
            if account.current_tier != old_tier:
                old_idx = next((i for i, t in enumerate(TIERS) if t["name"] == old_tier), 0)
                new_idx = next((i for i, t in enumerate(TIERS) if t["name"] == account.current_tier), 0)
                if new_idx > old_idx:
                    upgrades += 1
                else:
                    downgrades += 1
            else:
                unchanged += 1

        return {
            "total_accounts": len(accounts),
            "upgrades": upgrades,
            "downgrades": downgrades,
            "unchanged": unchanged,
        }

    @staticmethod
    def get_loyalty_summary(db: Session, restaurant_uid: str) -> dict:
        """Get aggregated loyalty stats for a restaurant."""
        accounts = LoyaltyService.get_accounts(db, restaurant_uid)

        # Enrich with supplier names
        enriched = []
        active_tiers = {}
        total_savings = 0.0

        for acct in accounts:
            supplier = db.query(SupplierDB).filter(SupplierDB.uid == acct.supplier_uid).first()
            supplier_name = supplier.name if supplier else acct.supplier_uid

            # Calculate next tier info
            next_t = _next_tier(acct.current_tier)
            next_tier_name = next_t["name"] if next_t else None
            orders_to_next = (next_t["min_orders"] - acct.orders_90d) if next_t else None

            # Calculate savings from discount
            acct_savings = db.query(func.sum(LoyaltyTransactionDB.discount_applied)).filter(
                LoyaltyTransactionDB.account_uid == acct.uid,
            ).scalar() or 0.0
            total_savings += acct_savings

            active_tiers.setdefault(acct.current_tier, 0)
            active_tiers[acct.current_tier] += 1

            enriched.append({
                "uid": acct.uid,
                "restaurant_uid": acct.restaurant_uid,
                "supplier_uid": acct.supplier_uid,
                "supplier_name": supplier_name,
                "current_tier": acct.current_tier,
                "orders_90d": acct.orders_90d,
                "total_orders": acct.total_orders,
                "total_spent": acct.total_spent,
                "discount_pct": acct.discount_pct,
                "effective_fee": acct.effective_fee,
                "next_tier": next_tier_name,
                "orders_to_next_tier": max(0, orders_to_next) if orders_to_next is not None else None,
                "last_evaluated": acct.last_evaluated,
                "created_at": acct.created_at,
                "updated_at": acct.updated_at,
            })

        total_orders = sum(a.total_orders for a in accounts)
        total_spent = sum(a.total_spent for a in accounts)
        avg_discount = sum(a.discount_pct for a in accounts) / len(accounts) if accounts else 0.0

        return {
            "total_supplier_accounts": len(accounts),
            "active_tiers": active_tiers,
            "total_lifetime_orders": total_orders,
            "total_lifetime_spent": round(total_spent, 2),
            "total_savings": round(total_savings, 2),
            "avg_discount_pct": round(avg_discount, 2),
            "accounts": enriched,
        }
