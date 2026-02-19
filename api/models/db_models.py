"""
Forkast SQLAlchemy ORM Models
Maps core.py dataclasses to persistent SQLite tables
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime,
    Text, ForeignKey, JSON, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from api.database import Base


def generate_uid():
    return str(uuid.uuid4())[:8]


class RestaurantDB(Base):
    __tablename__ = "restaurants"

    uid = Column(String(8), primary_key=True, default=generate_uid)
    name = Column(String(255), nullable=False)
    restaurant_type = Column(String(50), default="casual_dining")
    cuisine = Column(String(50), default="mixed")
    city = Column(String(100), default="")
    country = Column(String(50), default="UAE")
    seats = Column(Integer, default=40)
    avg_daily_covers = Column(Integer, default=80)
    monthly_revenue = Column(Float, default=0.0)
    operating_hours = Column(String(20), default="10:00-23:00")
    staff_count = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.now)

    menu_items = relationship("MenuItemDB", back_populates="restaurant")
    orders = relationship("OrderDB", back_populates="restaurant")
    payments = relationship("PaymentDB", back_populates="restaurant")


class MenuItemDB(Base):
    __tablename__ = "menu_items"

    uid = Column(String(8), primary_key=True, default=generate_uid)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(50), default="")
    price = Column(Float, default=0.0)
    cost = Column(Float, default=0.0)
    prep_time_minutes = Column(Integer, default=15)
    ingredients = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    popularity_score = Column(Float, default=0.5)
    avg_daily_orders = Column(Float, default=0.0)
    food_cost_pct = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    restaurant = relationship("RestaurantDB", back_populates="menu_items")


class InventoryItemDB(Base):
    __tablename__ = "inventory_items"

    uid = Column(String(8), primary_key=True, default=generate_uid)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(50), default="dry_goods")
    unit = Column(String(20), default="kg")
    current_stock = Column(Float, default=0.0)
    min_stock = Column(Float, default=0.0)
    max_stock = Column(Float, default=0.0)
    reorder_point = Column(Float, default=0.0)
    unit_cost = Column(Float, default=0.0)
    shelf_life_days = Column(Integer, default=7)
    supplier_uid = Column(String(8), nullable=True)
    last_restock = Column(DateTime, nullable=True)
    daily_usage_avg = Column(Float, default=0.0)
    wastage_pct = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SupplierDB(Base):
    __tablename__ = "suppliers"

    uid = Column(String(8), primary_key=True, default=generate_uid)
    name = Column(String(255), nullable=False)
    tier = Column(String(20), default="standard")
    categories = Column(JSON, default=list)
    city = Column(String(100), default="")
    country = Column(String(50), default="UAE")
    lead_time_days = Column(Float, default=1.0)
    min_order_value = Column(Float, default=0.0)
    reliability_score = Column(Float, default=0.85)
    avg_fill_rate = Column(Float, default=0.90)
    contact_email = Column(String(255), default="")
    contact_phone = Column(String(50), default="")
    is_active = Column(Boolean, default=True)
    total_orders = Column(Integer, default=0)
    total_value = Column(Float, default=0.0)


class OrderDB(Base):
    __tablename__ = "orders"

    uid = Column(String(8), primary_key=True, default=generate_uid)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=False)
    order_date = Column(DateTime, default=datetime.now)
    channel = Column(String(20), default="dine_in")
    total_amount = Column(Float, default=0.0)
    covers = Column(Integer, default=1)
    table_number = Column(Integer, nullable=True)
    pos_reference = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    restaurant = relationship("RestaurantDB", back_populates="orders")
    items = relationship("OrderItemDB", back_populates="order", cascade="all, delete-orphan")


class OrderItemDB(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_uid = Column(String(8), ForeignKey("orders.uid"), nullable=False)
    menu_item_uid = Column(String(8), nullable=True)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0.0)
    total_price = Column(Float, default=0.0)

    order = relationship("OrderDB", back_populates="items")


class PaymentDB(Base):
    __tablename__ = "payments"

    uid = Column(String(8), primary_key=True, default=generate_uid)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=False)
    supplier_uid = Column(String(8), ForeignKey("suppliers.uid"), nullable=True)
    procurement_order_uid = Column(String(8), nullable=True)
    stripe_session_id = Column(String(255), nullable=True)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)  # Total charged to restaurant (supplier + fee)
    supplier_amount = Column(Float, nullable=False, default=0.0)  # Net amount to supplier
    forkast_fee = Column(Float, nullable=False, default=0.0)  # Forkast revenue
    forkast_fee_pct = Column(Float, nullable=False, default=15.0)  # Fee percentage
    currency = Column(String(10), default="aed")
    status = Column(String(30), default="pending")
    description = Column(Text, default="")
    stripe_receipt_url = Column(String(500), nullable=True)
    refund_id = Column(String(255), nullable=True)
    refund_amount = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    restaurant = relationship("RestaurantDB", back_populates="payments")
    supplier = relationship("SupplierDB")


class StaffClockEventDB(Base):
    __tablename__ = "staff_clock_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=False)
    staff_name = Column(String(255), nullable=False)
    role = Column(String(50), default="")
    event_type = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    pos_reference = Column(String(100), nullable=True)


class LoyaltyAccountDB(Base):
    __tablename__ = "loyalty_accounts"
    __table_args__ = (
        UniqueConstraint("restaurant_uid", "supplier_uid", name="uq_loyalty_rest_sup"),
    )

    uid = Column(String(8), primary_key=True, default=generate_uid)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=False)
    supplier_uid = Column(String(8), ForeignKey("suppliers.uid"), nullable=False)
    current_tier = Column(String(20), default="standard")
    orders_90d = Column(Integer, default=0)
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    discount_pct = Column(Float, default=0.0)
    effective_fee = Column(Float, default=15.0)
    last_evaluated = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    restaurant = relationship("RestaurantDB")
    supplier = relationship("SupplierDB")
    transactions = relationship("LoyaltyTransactionDB", back_populates="account", cascade="all, delete-orphan")


class LoyaltyTransactionDB(Base):
    __tablename__ = "loyalty_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_uid = Column(String(8), ForeignKey("loyalty_accounts.uid"), nullable=False)
    event_type = Column(String(30), nullable=False)  # payment_completed, tier_upgrade, tier_downgrade, decay_check
    payment_uid = Column(String(8), nullable=True)
    order_count = Column(Integer, default=0)
    old_tier = Column(String(20), default="standard")
    new_tier = Column(String(20), default="standard")
    amount = Column(Float, default=0.0)
    discount_applied = Column(Float, default=0.0)
    note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)

    account = relationship("LoyaltyAccountDB", back_populates="transactions")


class APIKeyDB(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)
    restaurant_uid = Column(String(8), ForeignKey("restaurants.uid"), nullable=True)
    permissions = Column(JSON, default=lambda: ["pos:read", "pos:write"])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    last_used_at = Column(DateTime, nullable=True)
    request_count = Column(Integer, default=0)
