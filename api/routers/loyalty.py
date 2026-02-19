"""
Forkast Loyalty Program Endpoints
Tier-based rewards for restaurant-supplier relationships
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.database import get_db
from api.auth import require_permission
from api.models.db_models import APIKeyDB
from api.models.schemas import (
    LoyaltyTierInfo, LoyaltyAccountResponse,
    LoyaltyTransactionResponse, LoyaltySummary,
)
from api.services.loyalty_service import LoyaltyService

router = APIRouter(prefix="/api/v1/loyalty", tags=["Loyalty Program"])


@router.get("/tiers", response_model=List[LoyaltyTierInfo])
def get_tiers():
    """Get loyalty tier definitions (thresholds and discounts)."""
    tiers = LoyaltyService.get_tier_definitions()
    return [
        LoyaltyTierInfo(
            name=t["name"],
            min_orders=t["min_orders"],
            discount_pct=t["discount"],
            effective_fee=t["fee"],
        )
        for t in tiers
    ]


@router.get("/summary", response_model=LoyaltySummary)
def loyalty_summary(
    restaurant_uid: str = Query(...),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """Get aggregated loyalty stats for a restaurant across all suppliers."""
    return LoyaltyService.get_loyalty_summary(db, restaurant_uid)


@router.get("/accounts", response_model=List[LoyaltyAccountResponse])
def list_loyalty_accounts(
    restaurant_uid: str = Query(...),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """List all loyalty accounts for a restaurant."""
    accounts = LoyaltyService.get_accounts(db, restaurant_uid)
    # Enrich with supplier names and next tier info
    from api.models.db_models import SupplierDB
    from api.services.loyalty_service import _next_tier
    results = []
    for acct in accounts:
        supplier = db.query(SupplierDB).filter(SupplierDB.uid == acct.supplier_uid).first()
        next_t = _next_tier(acct.current_tier)
        results.append(LoyaltyAccountResponse(
            uid=acct.uid,
            restaurant_uid=acct.restaurant_uid,
            supplier_uid=acct.supplier_uid,
            supplier_name=supplier.name if supplier else acct.supplier_uid,
            current_tier=acct.current_tier,
            orders_90d=acct.orders_90d,
            total_orders=acct.total_orders,
            total_spent=acct.total_spent,
            discount_pct=acct.discount_pct,
            effective_fee=acct.effective_fee,
            next_tier=next_t["name"] if next_t else None,
            orders_to_next_tier=max(0, next_t["min_orders"] - acct.orders_90d) if next_t else None,
            last_evaluated=acct.last_evaluated,
            created_at=acct.created_at,
            updated_at=acct.updated_at,
        ))
    return results


@router.get("/accounts/{supplier_uid}", response_model=LoyaltyAccountResponse)
def get_loyalty_account(
    supplier_uid: str,
    restaurant_uid: str = Query(...),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """Get a specific restaurant-supplier loyalty account."""
    acct = LoyaltyService.get_account(db, restaurant_uid, supplier_uid)
    if not acct:
        raise HTTPException(status_code=404, detail="Loyalty account not found")

    from api.models.db_models import SupplierDB
    from api.services.loyalty_service import _next_tier
    supplier = db.query(SupplierDB).filter(SupplierDB.uid == supplier_uid).first()
    next_t = _next_tier(acct.current_tier)

    return LoyaltyAccountResponse(
        uid=acct.uid,
        restaurant_uid=acct.restaurant_uid,
        supplier_uid=acct.supplier_uid,
        supplier_name=supplier.name if supplier else supplier_uid,
        current_tier=acct.current_tier,
        orders_90d=acct.orders_90d,
        total_orders=acct.total_orders,
        total_spent=acct.total_spent,
        discount_pct=acct.discount_pct,
        effective_fee=acct.effective_fee,
        next_tier=next_t["name"] if next_t else None,
        orders_to_next_tier=max(0, next_t["min_orders"] - acct.orders_90d) if next_t else None,
        last_evaluated=acct.last_evaluated,
        created_at=acct.created_at,
        updated_at=acct.updated_at,
    )


@router.get("/accounts/{supplier_uid}/history", response_model=List[LoyaltyTransactionResponse])
def get_loyalty_history(
    supplier_uid: str,
    restaurant_uid: str = Query(...),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """Get transaction history for a loyalty account."""
    acct = LoyaltyService.get_account(db, restaurant_uid, supplier_uid)
    if not acct:
        raise HTTPException(status_code=404, detail="Loyalty account not found")
    return LoyaltyService.get_account_history(db, acct.uid, limit)


@router.post("/evaluate")
def evaluate_all(
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:write")),
):
    """Force re-evaluate all loyalty tiers (admin/cron operation)."""
    result = LoyaltyService.evaluate_all_accounts(db)
    return result
