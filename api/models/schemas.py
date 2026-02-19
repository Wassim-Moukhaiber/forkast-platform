"""
Forkast API Pydantic Schemas
Request and response models for all endpoints
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


# --- Enums for API ---
class OrderChannelAPI(str, Enum):
    dine_in = "dine_in"
    takeaway = "takeaway"
    delivery = "delivery"
    catering = "catering"


class PaymentStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    succeeded = "succeeded"
    failed = "failed"
    refunded = "refunded"


# --- Order Schemas ---
class OrderItemCreate(BaseModel):
    menu_item_uid: Optional[str] = None
    item_name: str
    quantity: int = 1
    unit_price: float


class OrderCreate(BaseModel):
    restaurant_uid: str
    channel: OrderChannelAPI = OrderChannelAPI.dine_in
    items: List[OrderItemCreate]
    covers: int = 1
    table_number: Optional[int] = None
    pos_reference: Optional[str] = None


class OrderItemResponse(BaseModel):
    item_name: str
    quantity: int
    unit_price: float
    total_price: float
    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    uid: str
    restaurant_uid: str
    order_date: datetime
    channel: str
    total_amount: float
    covers: int
    table_number: Optional[int] = None
    pos_reference: Optional[str] = None
    items: List[OrderItemResponse] = []
    created_at: datetime
    model_config = {"from_attributes": True}


# --- Menu Schemas ---
class MenuItemSync(BaseModel):
    name: str
    category: str = ""
    price: float = 0.0
    cost: float = 0.0
    prep_time_minutes: int = 15
    ingredients: List[str] = []
    is_active: bool = True
    popularity_score: float = 0.5
    avg_daily_orders: float = 0.0


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    prep_time_minutes: Optional[int] = None
    ingredients: Optional[List[str]] = None
    is_active: Optional[bool] = None


class MenuItemResponse(BaseModel):
    uid: str
    restaurant_uid: str
    name: str
    category: str
    price: float
    cost: float
    prep_time_minutes: int
    ingredients: list
    is_active: bool
    popularity_score: float
    avg_daily_orders: float
    food_cost_pct: float
    model_config = {"from_attributes": True}


class MenuSyncRequest(BaseModel):
    restaurant_uid: str
    items: List[MenuItemSync]


# --- Inventory Schemas ---
class InventoryUpdateItem(BaseModel):
    item_uid: Optional[str] = None
    name: Optional[str] = None
    new_stock: float
    unit: Optional[str] = None


class InventoryBatchUpdate(BaseModel):
    restaurant_uid: str
    items: List[InventoryUpdateItem]


class InventoryItemResponse(BaseModel):
    uid: str
    name: str
    category: str
    unit: str
    current_stock: float
    min_stock: float
    reorder_point: float
    unit_cost: float
    daily_usage_avg: float
    wastage_pct: float
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


# --- Staff Schemas ---
class StaffClockEvent(BaseModel):
    restaurant_uid: str
    staff_name: str
    role: str = ""
    event_type: str = "clock_in"
    timestamp: Optional[datetime] = None
    pos_reference: Optional[str] = None


class StaffClockResponse(BaseModel):
    id: int
    staff_name: str
    role: str
    event_type: str
    timestamp: datetime
    model_config = {"from_attributes": True}


# --- Payment Schemas ---
class PaymentCreate(BaseModel):
    restaurant_uid: str
    supplier_uid: Optional[str] = None
    procurement_order_uid: Optional[str] = None
    amount: float  # Supplier amount (before Forkast fee)
    currency: str = "aed"
    description: str = ""
    success_url: str = "http://localhost:8517"
    cancel_url: str = "http://localhost:8517"


class PaymentResponse(BaseModel):
    uid: str
    restaurant_uid: str
    supplier_uid: Optional[str] = None
    procurement_order_uid: Optional[str] = None
    stripe_session_id: Optional[str] = None
    amount: float  # Total charged (supplier + fee)
    supplier_amount: float = 0.0
    forkast_fee: float = 0.0
    forkast_fee_pct: float = 15.0
    currency: str
    status: str
    description: str
    stripe_receipt_url: Optional[str] = None
    refund_amount: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class PaymentStats(BaseModel):
    total_processed: float
    total_refunded: float
    total_pending: float
    total_forkast_revenue: float
    total_supplier_payouts: float
    count_succeeded: int
    count_failed: int
    count_pending: int
    count_refunded: int


class RevenueStats(BaseModel):
    """Forkast revenue model statistics."""
    total_transactions: int
    total_volume: float  # Total payment volume
    total_forkast_revenue: float
    total_supplier_payouts: float
    avg_fee_pct: float
    avg_transaction_size: float
    revenue_by_status: dict  # {status: revenue}
    recent_transactions: list  # Latest transactions with fee breakdown


# --- Loyalty Schemas ---
class LoyaltyTierInfo(BaseModel):
    name: str
    min_orders: int
    discount_pct: float
    effective_fee: float


class LoyaltyAccountResponse(BaseModel):
    uid: str
    restaurant_uid: str
    supplier_uid: str
    supplier_name: Optional[str] = None
    current_tier: str
    orders_90d: int
    total_orders: int
    total_spent: float
    discount_pct: float
    effective_fee: float
    next_tier: Optional[str] = None
    orders_to_next_tier: Optional[int] = None
    last_evaluated: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class LoyaltyTransactionResponse(BaseModel):
    id: int
    account_uid: str
    event_type: str
    payment_uid: Optional[str] = None
    order_count: int
    old_tier: str
    new_tier: str
    amount: float
    discount_applied: float
    note: str
    created_at: datetime
    model_config = {"from_attributes": True}


class LoyaltySummary(BaseModel):
    total_supplier_accounts: int
    active_tiers: dict  # {tier_name: count}
    total_lifetime_orders: int
    total_lifetime_spent: float
    total_savings: float  # Sum of all discount_applied
    avg_discount_pct: float
    accounts: List[LoyaltyAccountResponse]


# --- API Key Schemas ---
class APIKeyCreate(BaseModel):
    name: str
    restaurant_uid: Optional[str] = None
    permissions: List[str] = ["pos:read", "pos:write"]


class APIKeyResponse(BaseModel):
    id: int
    key_prefix: str
    name: str
    restaurant_uid: Optional[str] = None
    permissions: list
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None
    request_count: int
    model_config = {"from_attributes": True}


class APIKeyCreated(APIKeyResponse):
    """Returned only on creation -- includes the full plaintext key."""
    full_key: str


# --- Health Schemas ---
class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    stripe: str
    uptime_seconds: float


class APIInfoResponse(BaseModel):
    name: str
    version: str
    endpoints: dict
