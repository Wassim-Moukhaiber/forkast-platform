"""
Forkast Core Data Models
Restaurant, Menu, Inventory, Supplier, Order models
"""
from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid


# --- Enums ---

class RestaurantType(Enum):
    CASUAL_DINING = "casual_dining"
    FAST_CASUAL = "fast_casual"
    QUICK_SERVICE = "quick_service"
    CAFE = "cafe"
    FINE_DINING = "fine_dining"
    CLOUD_KITCHEN = "cloud_kitchen"


class CuisineType(Enum):
    ARABIC = "arabic"
    LEBANESE = "lebanese"
    INDIAN = "indian"
    TURKISH = "turkish"
    INTERNATIONAL = "international"
    ASIAN = "asian"
    ITALIAN = "italian"
    AMERICAN = "american"
    MIXED = "mixed"


class OrderChannel(Enum):
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"
    CATERING = "catering"


class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class SupplierTier(Enum):
    PREMIUM = "premium"
    STANDARD = "standard"
    ECONOMY = "economy"


class IngredientCategory(Enum):
    PROTEIN = "protein"
    DAIRY = "dairy"
    PRODUCE = "produce"
    GRAINS = "grains"
    SPICES = "spices"
    BEVERAGES = "beverages"
    OILS = "oils"
    FROZEN = "frozen"
    DRY_GOODS = "dry_goods"
    PACKAGING = "packaging"


class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# --- Core Models ---

@dataclass
class Restaurant:
    """Restaurant profile"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    restaurant_type: RestaurantType = RestaurantType.CASUAL_DINING
    cuisine: CuisineType = CuisineType.MIXED
    city: str = ""
    country: str = "UAE"
    seats: int = 40
    avg_daily_covers: int = 80
    monthly_revenue: float = 0.0
    operating_hours: str = "10:00-23:00"
    staff_count: int = 10
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "type": self.restaurant_type.value,
            "cuisine": self.cuisine.value,
            "city": self.city,
            "country": self.country,
            "seats": self.seats,
            "avg_daily_covers": self.avg_daily_covers,
            "monthly_revenue": self.monthly_revenue,
            "staff_count": self.staff_count
        }


@dataclass
class MenuItem:
    """Menu item"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    category: str = ""  # appetizer, main, dessert, beverage
    price: float = 0.0
    cost: float = 0.0
    prep_time_minutes: int = 15
    ingredients: List[str] = field(default_factory=list)
    is_active: bool = True
    popularity_score: float = 0.5  # 0-1
    avg_daily_orders: float = 0.0
    food_cost_pct: float = 0.0  # cost/price

    def __post_init__(self):
        if self.price > 0:
            self.food_cost_pct = (self.cost / self.price) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "cost": self.cost,
            "prep_time": self.prep_time_minutes,
            "food_cost_pct": round(self.food_cost_pct, 1),
            "popularity": self.popularity_score,
            "active": self.is_active
        }


@dataclass
class InventoryItem:
    """Inventory item"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    category: IngredientCategory = IngredientCategory.DRY_GOODS
    unit: str = "kg"
    current_stock: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    reorder_point: float = 0.0
    unit_cost: float = 0.0
    shelf_life_days: int = 7
    supplier_uid: Optional[str] = None
    last_restock: Optional[datetime] = None
    daily_usage_avg: float = 0.0
    wastage_pct: float = 0.0

    @property
    def stock_status(self) -> str:
        if self.current_stock <= 0:
            return "out_of_stock"
        elif self.current_stock <= self.reorder_point:
            return "low"
        elif self.current_stock >= self.max_stock * 0.9:
            return "overstocked"
        return "normal"

    @property
    def days_remaining(self) -> float:
        if self.daily_usage_avg > 0:
            return self.current_stock / self.daily_usage_avg
        return float('inf')

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "category": self.category.value,
            "unit": self.unit,
            "current_stock": self.current_stock,
            "min_stock": self.min_stock,
            "reorder_point": self.reorder_point,
            "unit_cost": self.unit_cost,
            "stock_status": self.stock_status,
            "days_remaining": round(self.days_remaining, 1),
            "wastage_pct": self.wastage_pct
        }


@dataclass
class Supplier:
    """Supplier profile"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    tier: SupplierTier = SupplierTier.STANDARD
    categories: List[IngredientCategory] = field(default_factory=list)
    city: str = ""
    country: str = "UAE"
    lead_time_days: float = 1.0
    min_order_value: float = 0.0
    reliability_score: float = 0.85  # 0-1
    avg_fill_rate: float = 0.90  # 0-1
    contact_email: str = ""
    contact_phone: str = ""
    is_active: bool = True
    total_orders: int = 0
    total_value: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "tier": self.tier.value,
            "categories": [c.value for c in self.categories],
            "lead_time_days": self.lead_time_days,
            "reliability_score": round(self.reliability_score * 100, 1),
            "fill_rate": round(self.avg_fill_rate * 100, 1),
            "total_orders": self.total_orders,
            "active": self.is_active
        }


@dataclass
class Order:
    """Customer order"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    restaurant_uid: str = ""
    order_date: datetime = field(default_factory=datetime.now)
    channel: OrderChannel = OrderChannel.DINE_IN
    items: List[Dict[str, Any]] = field(default_factory=list)  # [{menu_item_uid, qty, price}]
    total_amount: float = 0.0
    covers: int = 1
    table_number: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "date": self.order_date.isoformat(),
            "channel": self.channel.value,
            "items_count": len(self.items),
            "total": self.total_amount,
            "covers": self.covers
        }


@dataclass
class ProcurementOrder:
    """Procurement / Purchase order to supplier"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    supplier_uid: str = ""
    restaurant_uid: str = ""
    order_date: datetime = field(default_factory=datetime.now)
    expected_delivery: Optional[datetime] = None
    items: List[Dict[str, Any]] = field(default_factory=list)  # [{item_name, qty, unit, unit_cost}]
    total_value: float = 0.0
    status: str = "draft"  # draft, submitted, confirmed, delivered, cancelled
    auto_generated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "supplier_uid": self.supplier_uid,
            "date": self.order_date.isoformat(),
            "items_count": len(self.items),
            "total_value": self.total_value,
            "status": self.status,
            "auto_generated": self.auto_generated
        }


@dataclass
class StaffSchedule:
    """Staff scheduling entry"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    staff_name: str = ""
    role: str = ""  # chef, waiter, cashier, manager, kitchen_helper
    shift_date: date = field(default_factory=date.today)
    shift_start: str = "09:00"
    shift_end: str = "17:00"
    hours: float = 8.0
    hourly_rate: float = 0.0
    is_peak: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "staff_name": self.staff_name,
            "role": self.role,
            "date": self.shift_date.isoformat(),
            "shift": f"{self.shift_start}-{self.shift_end}",
            "hours": self.hours,
            "is_peak": self.is_peak
        }


@dataclass
class Alert:
    """Operational alert"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    severity: AlertSeverity = AlertSeverity.MEDIUM
    category: str = ""  # inventory, demand, labor, waste, supplier
    title: str = ""
    message: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    is_read: bool = False
    action_taken: bool = False
    recommended_action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "severity": self.severity.value,
            "category": self.category,
            "title": self.title,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "is_read": self.is_read,
            "action": self.recommended_action
        }


@dataclass
class DemandForecast:
    """Demand forecast result"""
    forecast_date: date = field(default_factory=date.today)
    predicted_covers: int = 0
    predicted_revenue: float = 0.0
    confidence_lower: float = 0.0
    confidence_upper: float = 0.0
    day_of_week: str = ""
    is_holiday: bool = False
    is_ramadan: bool = False
    weather_factor: float = 1.0
    channel_breakdown: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.forecast_date.isoformat(),
            "predicted_covers": self.predicted_covers,
            "predicted_revenue": self.predicted_revenue,
            "confidence_lower": self.confidence_lower,
            "confidence_upper": self.confidence_upper,
            "day_of_week": self.day_of_week,
            "is_holiday": self.is_holiday,
            "channels": self.channel_breakdown
        }
