"""
Forkast Data Service
CRUD operations for all database entities
"""
import secrets
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from api.models.db_models import (
    RestaurantDB, MenuItemDB, InventoryItemDB, SupplierDB,
    OrderDB, OrderItemDB, PaymentDB, StaffClockEventDB, APIKeyDB,
)
from api.auth import hash_api_key
from api.config import settings


class DataService:
    """Database CRUD operations."""

    # --- Orders ---
    @staticmethod
    def create_order(db: Session, order_data: dict) -> OrderDB:
        items_data = order_data.pop("items", [])
        total = sum(i["quantity"] * i["unit_price"] for i in items_data)

        order = OrderDB(
            restaurant_uid=order_data["restaurant_uid"],
            channel=order_data.get("channel", "dine_in"),
            total_amount=total,
            covers=order_data.get("covers", 1),
            table_number=order_data.get("table_number"),
            pos_reference=order_data.get("pos_reference"),
        )
        db.add(order)
        db.flush()

        for item in items_data:
            db_item = OrderItemDB(
                order_uid=order.uid,
                menu_item_uid=item.get("menu_item_uid"),
                item_name=item["item_name"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total_price=item["quantity"] * item["unit_price"],
            )
            db.add(db_item)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_orders(
        db: Session,
        restaurant_uid: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[OrderDB], int]:
        query = db.query(OrderDB)
        if restaurant_uid:
            query = query.filter(OrderDB.restaurant_uid == restaurant_uid)
        if date_from:
            query = query.filter(OrderDB.order_date >= date_from)
        if date_to:
            query = query.filter(OrderDB.order_date <= date_to)

        total = query.count()
        orders = query.order_by(OrderDB.order_date.desc()).offset(offset).limit(limit).all()
        return orders, total

    @staticmethod
    def get_order_by_uid(db: Session, uid: str) -> Optional[OrderDB]:
        return db.query(OrderDB).filter(OrderDB.uid == uid).first()

    # --- Menu ---
    @staticmethod
    def sync_menu(db: Session, restaurant_uid: str, items: list) -> List[MenuItemDB]:
        results = []
        for item_data in items:
            existing = db.query(MenuItemDB).filter(
                MenuItemDB.restaurant_uid == restaurant_uid,
                MenuItemDB.name == item_data["name"],
            ).first()

            if existing:
                for key, value in item_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                if existing.price > 0:
                    existing.food_cost_pct = (existing.cost / existing.price) * 100
                results.append(existing)
            else:
                food_cost_pct = 0.0
                price = item_data.get("price", 0)
                cost = item_data.get("cost", 0)
                if price > 0:
                    food_cost_pct = (cost / price) * 100
                new_item = MenuItemDB(
                    restaurant_uid=restaurant_uid,
                    food_cost_pct=food_cost_pct,
                    **item_data,
                )
                db.add(new_item)
                results.append(new_item)

        db.commit()
        for r in results:
            db.refresh(r)
        return results

    @staticmethod
    def get_menu(db: Session, restaurant_uid: str) -> List[MenuItemDB]:
        return db.query(MenuItemDB).filter(
            MenuItemDB.restaurant_uid == restaurant_uid
        ).all()

    @staticmethod
    def update_menu_item(db: Session, uid: str, updates: dict) -> Optional[MenuItemDB]:
        item = db.query(MenuItemDB).filter(MenuItemDB.uid == uid).first()
        if not item:
            return None
        for key, value in updates.items():
            if value is not None and hasattr(item, key):
                setattr(item, key, value)
        if item.price > 0:
            item.food_cost_pct = (item.cost / item.price) * 100
        item.updated_at = datetime.now()
        db.commit()
        db.refresh(item)
        return item

    # --- Inventory ---
    @staticmethod
    def batch_update_inventory(
        db: Session, restaurant_uid: str, items: list
    ) -> List[InventoryItemDB]:
        results = []
        for item_data in items:
            query = db.query(InventoryItemDB).filter(
                InventoryItemDB.restaurant_uid == restaurant_uid
            )
            if item_data.get("item_uid"):
                inv = query.filter(InventoryItemDB.uid == item_data["item_uid"]).first()
            elif item_data.get("name"):
                inv = query.filter(InventoryItemDB.name == item_data["name"]).first()
            else:
                continue

            if inv:
                inv.current_stock = item_data["new_stock"]
                if item_data.get("unit"):
                    inv.unit = item_data["unit"]
                inv.updated_at = datetime.now()
                results.append(inv)

        db.commit()
        for r in results:
            db.refresh(r)
        return results

    @staticmethod
    def get_inventory(db: Session, restaurant_uid: str) -> List[InventoryItemDB]:
        return db.query(InventoryItemDB).filter(
            InventoryItemDB.restaurant_uid == restaurant_uid
        ).all()

    # --- Staff ---
    @staticmethod
    def record_clock_event(db: Session, event_data: dict) -> StaffClockEventDB:
        event = StaffClockEventDB(
            restaurant_uid=event_data["restaurant_uid"],
            staff_name=event_data["staff_name"],
            role=event_data.get("role", ""),
            event_type=event_data["event_type"],
            timestamp=event_data.get("timestamp") or datetime.now(),
            pos_reference=event_data.get("pos_reference"),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_clock_events(
        db: Session, restaurant_uid: str, limit: int = 200
    ) -> List[StaffClockEventDB]:
        return db.query(StaffClockEventDB).filter(
            StaffClockEventDB.restaurant_uid == restaurant_uid
        ).order_by(StaffClockEventDB.timestamp.desc()).limit(limit).all()

    # --- Payments ---
    @staticmethod
    def create_payment(db: Session, payment_data: dict) -> PaymentDB:
        payment = PaymentDB(**payment_data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_payment_by_uid(db: Session, uid: str) -> Optional[PaymentDB]:
        return db.query(PaymentDB).filter(PaymentDB.uid == uid).first()

    @staticmethod
    def get_payment_by_session_id(db: Session, session_id: str) -> Optional[PaymentDB]:
        return db.query(PaymentDB).filter(PaymentDB.stripe_session_id == session_id).first()

    @staticmethod
    def update_payment(db: Session, payment: PaymentDB, updates: dict) -> PaymentDB:
        for key, value in updates.items():
            if hasattr(payment, key):
                setattr(payment, key, value)
        payment.updated_at = datetime.now()
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_payments(
        db: Session, restaurant_uid: Optional[str] = None, limit: int = 100
    ) -> List[PaymentDB]:
        query = db.query(PaymentDB)
        if restaurant_uid:
            query = query.filter(PaymentDB.restaurant_uid == restaurant_uid)
        return query.order_by(PaymentDB.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_payment_stats(db: Session, restaurant_uid: Optional[str] = None) -> dict:
        query = db.query(PaymentDB)
        if restaurant_uid:
            query = query.filter(PaymentDB.restaurant_uid == restaurant_uid)
        payments = query.all()
        return {
            "total_processed": sum(p.amount for p in payments if p.status == "succeeded"),
            "total_refunded": sum(p.refund_amount or 0 for p in payments if p.status == "refunded"),
            "total_pending": sum(p.amount for p in payments if p.status == "pending"),
            "total_forkast_revenue": sum(p.forkast_fee for p in payments if p.status == "succeeded"),
            "total_supplier_payouts": sum(p.supplier_amount for p in payments if p.status == "succeeded"),
            "count_succeeded": sum(1 for p in payments if p.status == "succeeded"),
            "count_failed": sum(1 for p in payments if p.status == "failed"),
            "count_pending": sum(1 for p in payments if p.status == "pending"),
            "count_refunded": sum(1 for p in payments if p.status == "refunded"),
        }

    @staticmethod
    def get_revenue_stats(db: Session, restaurant_uid: Optional[str] = None) -> dict:
        """Get Forkast revenue model statistics."""
        query = db.query(PaymentDB)
        if restaurant_uid:
            query = query.filter(PaymentDB.restaurant_uid == restaurant_uid)
        payments = query.order_by(PaymentDB.created_at.desc()).all()

        total_volume = sum(p.amount for p in payments)
        total_forkast = sum(p.forkast_fee for p in payments)
        total_supplier = sum(p.supplier_amount for p in payments)
        total_tx = len(payments)

        # Revenue breakdown by status
        revenue_by_status = {}
        for p in payments:
            revenue_by_status.setdefault(p.status, 0.0)
            revenue_by_status[p.status] += p.forkast_fee

        # Recent transactions with full fee breakdown
        recent = []
        for p in payments[:50]:
            recent.append({
                "uid": p.uid,
                "restaurant_uid": p.restaurant_uid,
                "supplier_uid": p.supplier_uid or "",
                "amount": p.amount,
                "supplier_amount": p.supplier_amount,
                "forkast_fee": p.forkast_fee,
                "forkast_fee_pct": p.forkast_fee_pct,
                "currency": p.currency,
                "status": p.status,
                "description": p.description or "",
                "created_at": p.created_at.isoformat() if p.created_at else "",
            })

        return {
            "total_transactions": total_tx,
            "total_volume": round(total_volume, 2),
            "total_forkast_revenue": round(total_forkast, 2),
            "total_supplier_payouts": round(total_supplier, 2),
            "avg_fee_pct": 15.0,
            "avg_transaction_size": round(total_volume / total_tx, 2) if total_tx > 0 else 0.0,
            "revenue_by_status": {k: round(v, 2) for k, v in revenue_by_status.items()},
            "recent_transactions": recent,
        }

    # --- API Keys ---
    @staticmethod
    def create_api_key(
        db: Session, name: str,
        restaurant_uid: Optional[str] = None,
        permissions: Optional[list] = None,
    ) -> Tuple[APIKeyDB, str]:
        """Create a new API key. Returns (db_record, plaintext_key)."""
        raw_key = settings.api_key_prefix + secrets.token_urlsafe(32)
        key_hash = hash_api_key(raw_key)
        key_prefix = raw_key[:12] + "..."

        db_key = APIKeyDB(
            key_hash=key_hash,
            key_prefix=key_prefix,
            name=name,
            restaurant_uid=restaurant_uid,
            permissions=permissions or ["pos:read", "pos:write"],
        )
        db.add(db_key)
        db.commit()
        db.refresh(db_key)
        return db_key, raw_key

    @staticmethod
    def list_api_keys(db: Session) -> List[APIKeyDB]:
        return db.query(APIKeyDB).order_by(APIKeyDB.created_at.desc()).all()

    @staticmethod
    def revoke_api_key(db: Session, key_id: int) -> bool:
        key = db.query(APIKeyDB).filter(APIKeyDB.id == key_id).first()
        if key:
            key.is_active = False
            db.commit()
            return True
        return False
