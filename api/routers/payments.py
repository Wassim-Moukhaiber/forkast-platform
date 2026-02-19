"""
Forkast Payment Endpoints
Stripe Checkout integration for procurement payments
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from api.database import get_db
from api.auth import require_permission
from api.models.db_models import APIKeyDB
from api.models.schemas import PaymentCreate, PaymentResponse, PaymentStats, RevenueStats
from api.services.stripe_service import StripeService
from api.services.data_service import DataService
from api.services.loyalty_service import LoyaltyService

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("/create-checkout", response_model=PaymentResponse, status_code=201)
def create_checkout(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:write")),
):
    """Create a Stripe Checkout Session for a procurement payment.

    The amount provided is the supplier amount. Forkast applies a 15% fee
    on top, so the restaurant is charged supplier_amount * 1.15.
    """
    if not StripeService.is_configured():
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured. Set FORKAST_STRIPE_SECRET_KEY environment variable.",
        )

    # Calculate fee breakdown using loyalty tier (defaults to 15% for new relationships)
    fee_pct = LoyaltyService.get_effective_fee(db, payment.restaurant_uid, payment.supplier_uid)
    supplier_amount = round(payment.amount, 2)
    forkast_fee = round(supplier_amount * fee_pct / 100, 2)
    total_charged = round(supplier_amount + forkast_fee, 2)

    db_payment = DataService.create_payment(db, {
        "restaurant_uid": payment.restaurant_uid,
        "supplier_uid": payment.supplier_uid,
        "procurement_order_uid": payment.procurement_order_uid,
        "amount": total_charged,
        "supplier_amount": supplier_amount,
        "forkast_fee": forkast_fee,
        "forkast_fee_pct": fee_pct,
        "currency": payment.currency,
        "status": "pending",
        "description": payment.description,
    })

    try:
        session = StripeService.create_checkout_session(
            amount_aed=total_charged,
            currency=payment.currency,
            description=payment.description or f"Forkast Payment {db_payment.uid}",
            success_url=payment.success_url,
            cancel_url=payment.cancel_url,
            metadata={
                "forkast_payment_uid": db_payment.uid,
                "restaurant_uid": payment.restaurant_uid,
                "supplier_amount": str(supplier_amount),
                "forkast_fee": str(forkast_fee),
            },
        )
    except Exception as e:
        DataService.update_payment(db, db_payment, {"status": "failed"})
        raise HTTPException(status_code=502, detail=f"Stripe error: {str(e)}")

    DataService.update_payment(db, db_payment, {
        "stripe_session_id": session.id,
        "status": "processing",
    })

    return db_payment


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events. Verified via Stripe signature."""
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature", "")

    try:
        event = StripeService.construct_webhook_event(payload, sig_header)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event.type == "checkout.session.completed":
        session = event.data.object
        payment = DataService.get_payment_by_session_id(db, session.id)
        if payment:
            DataService.update_payment(db, payment, {
                "status": "succeeded",
                "stripe_payment_intent_id": session.payment_intent,
                "stripe_receipt_url": getattr(session, "receipt_url", None),
            })
            # Record loyalty event if supplier is linked
            if payment.supplier_uid:
                default_fee = 15.0
                discount_saved = round(
                    payment.supplier_amount * (default_fee - payment.forkast_fee_pct) / 100, 2
                )
                LoyaltyService.record_payment(
                    db, payment.restaurant_uid, payment.supplier_uid,
                    payment.uid, payment.supplier_amount, discount_saved,
                )

    elif event.type == "checkout.session.expired":
        session = event.data.object
        payment = DataService.get_payment_by_session_id(db, session.id)
        if payment:
            DataService.update_payment(db, payment, {"status": "failed"})

    return {"status": "received"}


@router.get("/stats", response_model=PaymentStats)
def payment_stats(
    restaurant_uid: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """Get aggregated payment statistics."""
    return DataService.get_payment_stats(db, restaurant_uid)


@router.get("", response_model=List[PaymentResponse])
def list_payments(
    restaurant_uid: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """List payment transactions."""
    return DataService.get_payments(db, restaurant_uid, limit)


@router.get("/revenue", response_model=RevenueStats)
def revenue_stats(
    restaurant_uid: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """Get Forkast revenue model statistics from payment transactions."""
    return DataService.get_revenue_stats(db, restaurant_uid)


@router.get("/{uid}", response_model=PaymentResponse)
def get_payment(
    uid: str,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:read")),
):
    """Get payment details by UID."""
    payment = DataService.get_payment_by_uid(db, uid)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/{uid}/refund", response_model=PaymentResponse)
def refund_payment(
    uid: str,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("payments:write")),
):
    """Initiate a full refund for a payment."""
    payment = DataService.get_payment_by_uid(db, uid)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status != "succeeded":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot refund payment in status: {payment.status}",
        )
    if not payment.stripe_payment_intent_id:
        raise HTTPException(
            status_code=400,
            detail="No Stripe PaymentIntent associated with this payment",
        )

    try:
        refund = StripeService.create_refund(payment.stripe_payment_intent_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Stripe refund error: {str(e)}")

    DataService.update_payment(db, payment, {
        "status": "refunded",
        "refund_id": refund.id,
        "refund_amount": payment.amount,
    })
    return payment
