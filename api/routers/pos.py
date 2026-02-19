"""
Forkast POS Integration Endpoints
REST API for any POS system to sync data with Forkast
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.database import get_db
from api.auth import require_permission
from api.models.db_models import APIKeyDB, StaffClockEventDB
from api.models.schemas import (
    OrderCreate, OrderResponse,
    MenuSyncRequest, MenuItemResponse, MenuItemUpdate,
    InventoryBatchUpdate, InventoryItemResponse,
    StaffClockEvent, StaffClockResponse,
)
from api.services.data_service import DataService

router = APIRouter(prefix="/api/v1/pos", tags=["POS Integration"])


# --- Orders ---
@router.post("/orders", response_model=OrderResponse, status_code=201)
def submit_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:write")),
):
    """Submit a new order from POS system."""
    result = DataService.create_order(db, order.model_dump())
    return result


@router.get("/orders", response_model=List[OrderResponse])
def list_orders(
    restaurant_uid: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:read")),
):
    """List orders with optional date range filters."""
    orders, total = DataService.get_orders(
        db, restaurant_uid, date_from, date_to, limit, offset
    )
    return orders


@router.get("/orders/{uid}", response_model=OrderResponse)
def get_order(
    uid: str,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:read")),
):
    """Get a single order by UID."""
    order = DataService.get_order_by_uid(db, uid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# --- Menu ---
@router.post("/menu/sync", response_model=List[MenuItemResponse])
def sync_menu(
    request: MenuSyncRequest,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:write")),
):
    """Sync menu items from POS. Upserts by name."""
    items = [i.model_dump() for i in request.items]
    return DataService.sync_menu(db, request.restaurant_uid, items)


@router.get("/menu", response_model=List[MenuItemResponse])
def get_menu(
    restaurant_uid: str = Query(...),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:read")),
):
    """Get current menu for a restaurant."""
    return DataService.get_menu(db, restaurant_uid)


@router.put("/menu/{uid}", response_model=MenuItemResponse)
def update_menu_item(
    uid: str,
    updates: MenuItemUpdate,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:write")),
):
    """Update a single menu item."""
    result = DataService.update_menu_item(db, uid, updates.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return result


# --- Inventory ---
@router.post("/inventory/update", response_model=List[InventoryItemResponse])
def update_inventory(
    batch: InventoryBatchUpdate,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:write")),
):
    """Batch update inventory levels from POS."""
    items = [i.model_dump() for i in batch.items]
    return DataService.batch_update_inventory(db, batch.restaurant_uid, items)


@router.get("/inventory", response_model=List[InventoryItemResponse])
def get_inventory(
    restaurant_uid: str = Query(...),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:read")),
):
    """Get current inventory levels."""
    return DataService.get_inventory(db, restaurant_uid)


# --- Staff ---
@router.post("/staff/clock-in", response_model=StaffClockResponse, status_code=201)
def staff_clock_in(
    event: StaffClockEvent,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:write")),
):
    """Record a staff clock-in event."""
    data = event.model_dump()
    data["event_type"] = "clock_in"
    return DataService.record_clock_event(db, data)


@router.post("/staff/clock-out", response_model=StaffClockResponse, status_code=201)
def staff_clock_out(
    event: StaffClockEvent,
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:write")),
):
    """Record a staff clock-out event."""
    data = event.model_dump()
    data["event_type"] = "clock_out"
    return DataService.record_clock_event(db, data)


@router.get("/staff/schedule", response_model=List[StaffClockResponse])
def get_staff_schedule(
    restaurant_uid: str = Query(...),
    db: Session = Depends(get_db),
    api_key: APIKeyDB = Depends(require_permission("pos:read")),
):
    """Get recent staff clock events."""
    return DataService.get_clock_events(db, restaurant_uid)


# --- Forecasts ---
@router.get("/forecasts")
def get_forecasts(
    restaurant_uid: str = Query(...),
    days_ahead: int = Query(14, ge=1, le=30),
    api_key: APIKeyDB = Depends(require_permission("pos:read")),
):
    """Get demand forecasts using the Forkast AI engine."""
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    from data.demo_generator import DemoDataGenerator
    from forecasting.demand_engine import DemandForecastEngine

    gen = DemoDataGenerator()
    data = gen.generate_all()
    engine = DemandForecastEngine()
    engine.train(data["historical_orders"])
    forecasts = engine.forecast(days_ahead=days_ahead)
    return [f.to_dict() for f in forecasts]
