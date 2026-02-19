"""
Forkast API Health & Info Endpoints
"""
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import get_db
from api.config import settings
from api.models.schemas import HealthResponse, APIInfoResponse
from api.services.stripe_service import StripeService

router = APIRouter(prefix="/api/v1", tags=["Health"])

_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    stripe_status = "configured" if StripeService.is_configured() else "not_configured"

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        database=db_status,
        stripe=stripe_status,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


@router.get("/info", response_model=APIInfoResponse)
def api_info():
    return APIInfoResponse(
        name=settings.app_name,
        version=settings.app_version,
        endpoints={
            "pos_orders": "/api/v1/pos/orders",
            "pos_menu": "/api/v1/pos/menu",
            "pos_inventory": "/api/v1/pos/inventory",
            "pos_staff_clock_in": "/api/v1/pos/staff/clock-in",
            "pos_staff_clock_out": "/api/v1/pos/staff/clock-out",
            "pos_forecasts": "/api/v1/pos/forecasts",
            "payments": "/api/v1/payments",
            "payments_checkout": "/api/v1/payments/create-checkout",
            "payments_webhook": "/api/v1/payments/webhook",
            "health": "/api/v1/health",
            "docs": "/docs",
        },
    )
