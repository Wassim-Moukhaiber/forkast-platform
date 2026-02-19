"""
Forkast Demo Data Generator
Generates realistic restaurant operations data for MENA region
"""
import random
import math
from datetime import datetime, timedelta, date
from typing import List, Dict, Tuple
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.core import (
    Restaurant, MenuItem, InventoryItem, Supplier, Order,
    ProcurementOrder, StaffSchedule, Alert, DemandForecast,
    RestaurantType, CuisineType, OrderChannel, SupplierTier,
    IngredientCategory, AlertSeverity, DayOfWeek
)


class DemoDataGenerator:
    """Generate comprehensive demo data for Forkast platform"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.restaurant = None

    def generate_restaurant(self) -> Restaurant:
        """Generate a demo restaurant"""
        self.restaurant = Restaurant(
            uid="REST-001",
            name="Al Safwa Kitchen",
            restaurant_type=RestaurantType.CASUAL_DINING,
            cuisine=CuisineType.ARABIC,
            city="Dubai",
            country="UAE",
            seats=65,
            avg_daily_covers=95,
            monthly_revenue=85000.0,
            operating_hours="11:00-23:00",
            staff_count=18
        )
        return self.restaurant

    def generate_menu(self) -> List[MenuItem]:
        """Generate a realistic Arabic restaurant menu"""
        menu_data = [
            # Appetizers
            ("Hummus Classic", "appetizer", 22, 5.5, 10, ["chickpeas", "tahini", "lemon", "garlic", "olive_oil"], 0.82),
            ("Fattoush Salad", "appetizer", 25, 6.0, 8, ["lettuce", "tomato", "cucumber", "pita", "sumac"], 0.75),
            ("Mutabal", "appetizer", 24, 5.8, 10, ["eggplant", "tahini", "garlic", "lemon"], 0.70),
            ("Falafel Plate", "appetizer", 20, 4.5, 12, ["chickpeas", "herbs", "spices", "oil"], 0.88),
            ("Vine Leaves", "appetizer", 28, 7.0, 15, ["grape_leaves", "rice", "lamb", "spices"], 0.65),
            ("Kibbeh", "appetizer", 30, 8.5, 18, ["bulgur", "lamb", "onion", "pine_nuts"], 0.60),
            # Mains
            ("Mixed Grill Platter", "main", 75, 22.0, 25, ["lamb", "chicken", "beef", "rice", "vegetables"], 0.95),
            ("Lamb Ouzi", "main", 65, 20.0, 30, ["lamb", "rice", "nuts", "spices"], 0.78),
            ("Chicken Shawarma", "main", 38, 10.0, 15, ["chicken", "garlic_sauce", "pickles", "bread"], 0.92),
            ("Grilled Sea Bass", "main", 85, 28.0, 20, ["sea_bass", "lemon", "herbs", "rice"], 0.55),
            ("Mansaf", "main", 70, 22.0, 35, ["lamb", "jameed", "rice", "nuts"], 0.72),
            ("Chicken Biryani", "main", 45, 12.0, 25, ["chicken", "rice", "spices", "onion"], 0.85),
            ("Kebab Halabi", "main", 55, 16.0, 20, ["lamb", "spices", "tomato", "pepper"], 0.80),
            ("Kofta Plate", "main", 42, 11.0, 18, ["beef", "onion", "spices", "rice"], 0.78),
            # Desserts
            ("Kunafa", "dessert", 32, 8.0, 15, ["cheese", "semolina", "syrup", "pistachios"], 0.88),
            ("Umm Ali", "dessert", 28, 6.0, 20, ["bread", "milk", "cream", "nuts", "raisins"], 0.72),
            ("Baklava Assorted", "dessert", 35, 9.0, 5, ["filo", "nuts", "butter", "syrup"], 0.65),
            # Beverages
            ("Fresh Lemon Mint", "beverage", 15, 2.5, 5, ["lemon", "mint", "sugar", "water"], 0.90),
            ("Arabic Coffee", "beverage", 12, 1.8, 3, ["coffee", "cardamom", "saffron"], 0.95),
            ("Mango Lassi", "beverage", 18, 4.0, 5, ["mango", "yogurt", "sugar", "ice"], 0.75),
            ("Jallab", "beverage", 16, 3.0, 5, ["dates", "grape_molasses", "rose_water", "pine_nuts"], 0.70),
        ]

        menu = []
        for name, cat, price, cost, prep, ingredients, popularity in menu_data:
            item = MenuItem(
                name=name,
                category=cat,
                price=price,
                cost=cost,
                prep_time_minutes=prep,
                ingredients=ingredients,
                popularity_score=popularity,
                avg_daily_orders=round(popularity * random.uniform(8, 25), 1)
            )
            menu.append(item)

        return menu

    def generate_inventory(self, menu: List[MenuItem]) -> List[InventoryItem]:
        """Generate inventory items based on menu"""
        inventory_data = [
            ("Chicken Breast", IngredientCategory.PROTEIN, "kg", 45, 15, 80, 25, 18.0, 5, 8.5),
            ("Lamb Shoulder", IngredientCategory.PROTEIN, "kg", 30, 10, 60, 18, 35.0, 4, 5.2),
            ("Ground Beef", IngredientCategory.PROTEIN, "kg", 25, 8, 50, 15, 28.0, 3, 4.8),
            ("Sea Bass Fillet", IngredientCategory.PROTEIN, "kg", 12, 5, 25, 8, 55.0, 2, 3.0),
            ("Basmati Rice", IngredientCategory.GRAINS, "kg", 80, 20, 150, 40, 4.5, 90, 12.0),
            ("Bulgur Wheat", IngredientCategory.GRAINS, "kg", 20, 5, 40, 10, 3.8, 60, 2.5),
            ("Pita Bread", IngredientCategory.GRAINS, "pcs", 200, 50, 400, 100, 0.5, 3, 35.0),
            ("Chickpeas", IngredientCategory.DRY_GOODS, "kg", 30, 10, 60, 15, 3.2, 180, 4.5),
            ("Tahini", IngredientCategory.DRY_GOODS, "kg", 8, 3, 15, 5, 12.0, 120, 1.2),
            ("Olive Oil", IngredientCategory.OILS, "L", 15, 5, 30, 8, 18.0, 365, 2.5),
            ("Tomatoes", IngredientCategory.PRODUCE, "kg", 25, 8, 50, 15, 5.5, 5, 6.0),
            ("Cucumbers", IngredientCategory.PRODUCE, "kg", 15, 5, 30, 10, 3.8, 5, 3.5),
            ("Onions", IngredientCategory.PRODUCE, "kg", 20, 8, 40, 12, 2.5, 14, 4.0),
            ("Lemons", IngredientCategory.PRODUCE, "kg", 10, 3, 20, 6, 6.0, 10, 2.0),
            ("Mixed Herbs", IngredientCategory.PRODUCE, "kg", 5, 2, 10, 3, 15.0, 3, 1.5),
            ("Garlic", IngredientCategory.PRODUCE, "kg", 8, 3, 15, 5, 8.0, 21, 1.2),
            ("Arabic Spice Mix", IngredientCategory.SPICES, "kg", 3, 1, 8, 2, 25.0, 180, 0.4),
            ("Saffron", IngredientCategory.SPICES, "g", 50, 10, 100, 20, 2.5, 365, 5.0),
            ("Yogurt", IngredientCategory.DAIRY, "kg", 20, 8, 40, 12, 4.5, 7, 5.0),
            ("Cream", IngredientCategory.DAIRY, "L", 10, 4, 20, 6, 8.0, 5, 2.5),
            ("Cheese Mix", IngredientCategory.DAIRY, "kg", 12, 5, 25, 8, 22.0, 14, 3.0),
            ("Pine Nuts", IngredientCategory.DRY_GOODS, "kg", 3, 1, 8, 2, 65.0, 180, 0.5),
            ("Pistachios", IngredientCategory.DRY_GOODS, "kg", 4, 1, 10, 3, 45.0, 180, 0.6),
            ("Takeaway Containers", IngredientCategory.PACKAGING, "pcs", 300, 100, 600, 200, 0.35, 365, 45.0),
            ("Paper Bags", IngredientCategory.PACKAGING, "pcs", 200, 80, 500, 150, 0.15, 365, 30.0),
        ]

        inventory = []
        for name, cat, unit, stock, min_s, max_s, reorder, cost, shelf, usage in inventory_data:
            # Add some randomness
            stock_var = stock * random.uniform(0.6, 1.2)
            wastage = random.uniform(2, 12) if cat in [IngredientCategory.PRODUCE, IngredientCategory.DAIRY, IngredientCategory.PROTEIN] else random.uniform(0.5, 3)

            item = InventoryItem(
                name=name,
                category=cat,
                unit=unit,
                current_stock=round(stock_var, 1),
                min_stock=min_s,
                max_stock=max_s,
                reorder_point=reorder,
                unit_cost=cost,
                shelf_life_days=shelf,
                daily_usage_avg=usage,
                wastage_pct=round(wastage, 1),
                last_restock=datetime.now() - timedelta(days=random.randint(1, 7))
            )
            inventory.append(item)

        return inventory

    def generate_suppliers(self) -> List[Supplier]:
        """Generate supplier profiles"""
        suppliers_data = [
            ("Al Jazira Foods", SupplierTier.PREMIUM, [IngredientCategory.PROTEIN, IngredientCategory.DAIRY], "Dubai", 1.0, 500, 0.95, 0.97),
            ("Gulf Fresh Produce", SupplierTier.STANDARD, [IngredientCategory.PRODUCE], "Sharjah", 0.5, 200, 0.88, 0.92),
            ("Emirates Dry Goods", SupplierTier.STANDARD, [IngredientCategory.DRY_GOODS, IngredientCategory.GRAINS, IngredientCategory.SPICES], "Dubai", 2.0, 300, 0.92, 0.94),
            ("MENA Oils & Condiments", SupplierTier.ECONOMY, [IngredientCategory.OILS, IngredientCategory.SPICES], "Abu Dhabi", 3.0, 150, 0.82, 0.85),
            ("PackRight Solutions", SupplierTier.STANDARD, [IngredientCategory.PACKAGING], "Dubai", 2.0, 100, 0.90, 0.93),
            ("Seafood Direct", SupplierTier.PREMIUM, [IngredientCategory.PROTEIN], "Dubai", 0.5, 400, 0.93, 0.96),
            ("Farm to Table UAE", SupplierTier.PREMIUM, [IngredientCategory.PRODUCE, IngredientCategory.DAIRY], "Al Ain", 1.5, 250, 0.90, 0.91),
        ]

        suppliers = []
        for name, tier, cats, city, lead, min_order, reliability, fill in suppliers_data:
            supplier = Supplier(
                name=name,
                tier=tier,
                categories=cats,
                city=city,
                lead_time_days=lead,
                min_order_value=min_order,
                reliability_score=reliability,
                avg_fill_rate=fill,
                total_orders=random.randint(50, 300),
                total_value=random.uniform(15000, 120000)
            )
            suppliers.append(supplier)

        return suppliers

    def generate_historical_orders(self, menu: List[MenuItem], days: int = 90) -> List[Dict[str, Any]]:
        """Generate historical order data for demand forecasting"""
        orders = []
        base_date = datetime.now() - timedelta(days=days)

        for day_offset in range(days):
            current_date = base_date + timedelta(days=day_offset)
            dow = current_date.weekday()

            # Base covers with day-of-week pattern (MENA: Thu-Fri-Sat peak)
            base_covers = 85
            dow_factors = {0: 0.75, 1: 0.80, 2: 0.85, 3: 0.95, 4: 1.25, 5: 1.30, 6: 0.90}
            day_factor = dow_factors.get(dow, 1.0)

            # Monthly seasonality
            month = current_date.month
            month_factors = {1: 0.85, 2: 0.90, 3: 1.05, 4: 1.0, 5: 0.95, 6: 0.80,
                           7: 0.75, 8: 0.78, 9: 0.85, 10: 1.0, 11: 1.10, 12: 1.20}
            month_factor = month_factors.get(month, 1.0)

            # Trend (slight upward)
            trend = 1.0 + (day_offset / days) * 0.08

            # Random noise
            noise = random.gauss(1.0, 0.1)

            total_covers = max(20, int(base_covers * day_factor * month_factor * trend * noise))

            # Channel split
            dine_in_pct = random.uniform(0.45, 0.55)
            delivery_pct = random.uniform(0.25, 0.35)
            takeaway_pct = 1 - dine_in_pct - delivery_pct

            # Revenue per cover
            avg_check = random.gauss(52, 8)

            daily_data = {
                "date": current_date.date().isoformat(),
                "day_of_week": current_date.strftime("%A"),
                "total_covers": total_covers,
                "dine_in": int(total_covers * dine_in_pct),
                "delivery": int(total_covers * delivery_pct),
                "takeaway": int(total_covers * takeaway_pct),
                "total_revenue": round(total_covers * avg_check, 2),
                "avg_check": round(avg_check, 2),
                "orders_count": int(total_covers * random.uniform(0.6, 0.8)),
                "peak_hour_covers": int(total_covers * random.uniform(0.25, 0.35)),
                "food_waste_kg": round(total_covers * random.uniform(0.08, 0.15), 1),
                "food_cost_pct": round(random.uniform(28, 35), 1),
                "labor_cost_pct": round(random.uniform(22, 28), 1),
            }

            # Item-level data
            item_orders = {}
            for item in menu:
                qty = max(0, int(item.avg_daily_orders * day_factor * noise * random.uniform(0.7, 1.3)))
                if qty > 0:
                    item_orders[item.name] = qty

            daily_data["item_orders"] = item_orders
            orders.append(daily_data)

        return orders

    def generate_alerts(self, inventory: List[InventoryItem]) -> List[Alert]:
        """Generate operational alerts based on current state"""
        alerts = []

        # Low stock alerts
        for item in inventory:
            if item.stock_status == "low":
                alerts.append(Alert(
                    severity=AlertSeverity.HIGH,
                    category="inventory",
                    title=f"Low Stock: {item.name}",
                    message=f"{item.name} is at {item.current_stock} {item.unit} (below reorder point of {item.reorder_point} {item.unit}). Estimated {item.days_remaining:.0f} days remaining.",
                    recommended_action=f"Order {item.reorder_point * 2 - item.current_stock:.0f} {item.unit} from supplier"
                ))
            elif item.stock_status == "out_of_stock":
                alerts.append(Alert(
                    severity=AlertSeverity.CRITICAL,
                    category="inventory",
                    title=f"OUT OF STOCK: {item.name}",
                    message=f"{item.name} is out of stock! This affects menu items requiring this ingredient.",
                    recommended_action=f"Place emergency order immediately"
                ))

        # High wastage alert
        high_waste_items = [i for i in inventory if i.wastage_pct > 8]
        if high_waste_items:
            alerts.append(Alert(
                severity=AlertSeverity.MEDIUM,
                category="waste",
                title="High Food Waste Detected",
                message=f"{len(high_waste_items)} ingredients have wastage above 8%. Top: {high_waste_items[0].name} at {high_waste_items[0].wastage_pct}%",
                recommended_action="Review portion sizes and storage practices for flagged items"
            ))

        # Demand surge alert
        alerts.append(Alert(
            severity=AlertSeverity.MEDIUM,
            category="demand",
            title="Weekend Demand Surge Expected",
            message="AI forecasts 25% higher covers this Thursday-Saturday based on historical patterns and local events.",
            recommended_action="Increase prep quantities for top 5 items; schedule 2 additional staff"
        ))

        # Labor optimization
        alerts.append(Alert(
            severity=AlertSeverity.LOW,
            category="labor",
            title="Labor Optimization Opportunity",
            message="Tuesday and Wednesday show consistent overstaffing (3.2 staff/hour vs 2.1 needed). Consider schedule adjustment.",
            recommended_action="Reduce Tuesday-Wednesday shifts by 1 staff member during 14:00-17:00"
        ))

        return alerts

    def generate_staff_schedule(self) -> List[StaffSchedule]:
        """Generate weekly staff schedule"""
        staff_roles = [
            ("Ahmed K.", "head_chef", 35),
            ("Fatima M.", "sous_chef", 28),
            ("Hassan R.", "line_cook", 22),
            ("Omar S.", "line_cook", 22),
            ("Noura A.", "prep_cook", 18),
            ("Khalid W.", "waiter", 18),
            ("Sara B.", "waiter", 18),
            ("Ali H.", "waiter", 18),
            ("Maryam T.", "waitress", 18),
            ("Yousef D.", "cashier", 20),
            ("Layla F.", "host", 18),
            ("Ibrahim N.", "kitchen_helper", 15),
            ("Rania Q.", "kitchen_helper", 15),
            ("Tariq J.", "dishwasher", 14),
            ("Samira L.", "manager", 40),
            ("Nasser G.", "delivery_driver", 16),
            ("Huda E.", "delivery_driver", 16),
            ("Zain P.", "barista", 18),
        ]

        schedules = []
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())

        for day_offset in range(7):
            shift_date = start_of_week + timedelta(days=day_offset)
            dow = shift_date.weekday()
            is_peak = dow in [3, 4, 5]  # Thu, Fri, Sat

            for name, role, rate in staff_roles:
                # Not everyone works every day
                if random.random() < (0.85 if is_peak else 0.70):
                    if role in ["head_chef", "manager"]:
                        start, end = "10:00", "22:00"
                        hours = 12
                    elif role in ["delivery_driver"]:
                        start, end = "11:00", "23:00"
                        hours = 12
                    elif is_peak:
                        start = random.choice(["10:00", "11:00"])
                        end = random.choice(["22:00", "23:00"])
                        hours = 12
                    else:
                        shift_type = random.choice(["morning", "evening"])
                        if shift_type == "morning":
                            start, end = "10:00", "17:00"
                            hours = 7
                        else:
                            start, end = "16:00", "23:00"
                            hours = 7

                    schedules.append(StaffSchedule(
                        staff_name=name,
                        role=role,
                        shift_date=shift_date,
                        shift_start=start,
                        shift_end=end,
                        hours=hours,
                        hourly_rate=rate,
                        is_peak=is_peak
                    ))

        return schedules

    def generate_all(self) -> Dict[str, Any]:
        """Generate all demo data"""
        restaurant = self.generate_restaurant()
        menu = self.generate_menu()
        inventory = self.generate_inventory(menu)
        suppliers = self.generate_suppliers()
        historical_orders = self.generate_historical_orders(menu, days=90)
        alerts = self.generate_alerts(inventory)
        staff_schedule = self.generate_staff_schedule()

        return {
            "restaurant": restaurant,
            "menu": menu,
            "inventory": inventory,
            "suppliers": suppliers,
            "historical_orders": historical_orders,
            "alerts": alerts,
            "staff_schedule": staff_schedule
        }
