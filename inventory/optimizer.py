"""
Forkast Inventory Optimizer
AI-driven inventory management and procurement automation
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.core import (
    InventoryItem, Supplier, ProcurementOrder, Alert,
    AlertSeverity, IngredientCategory
)


class InventoryOptimizer:
    """Optimizes inventory levels and generates procurement recommendations"""

    def __init__(self):
        self.safety_stock_multiplier = 1.5

    def analyze_inventory(self, inventory: List[InventoryItem]) -> Dict[str, Any]:
        total_value = sum(i.current_stock * i.unit_cost for i in inventory)
        low_stock = [i for i in inventory if i.stock_status == "low"]
        out_of_stock = [i for i in inventory if i.stock_status == "out_of_stock"]
        overstocked = [i for i in inventory if i.stock_status == "overstocked"]
        high_waste = [i for i in inventory if i.wastage_pct > 8]

        by_category = {}
        for item in inventory:
            cat = item.category.value
            if cat not in by_category:
                by_category[cat] = {"count": 0, "value": 0, "avg_waste": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["value"] += item.current_stock * item.unit_cost
            by_category[cat]["avg_waste"] += item.wastage_pct
        for cat in by_category:
            if by_category[cat]["count"] > 0:
                by_category[cat]["avg_waste"] = round(by_category[cat]["avg_waste"] / by_category[cat]["count"], 1)
                by_category[cat]["value"] = round(by_category[cat]["value"], 2)

        score = 100
        score -= sum(1 for i in inventory if i.stock_status == "out_of_stock") * 15
        score -= sum(1 for i in inventory if i.stock_status == "low") * 5
        score -= sum(1 for i in inventory if i.stock_status == "overstocked") * 3
        score -= sum(1 for i in inventory if i.wastage_pct > 10) * 4
        score = max(0, min(100, score))

        return {
            "total_items": len(inventory),
            "total_value": round(total_value, 2),
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "overstocked_count": len(overstocked),
            "high_waste_count": len(high_waste),
            "low_stock_items": [i.name for i in low_stock],
            "out_of_stock_items": [i.name for i in out_of_stock],
            "by_category": by_category,
            "avg_wastage": round(sum(i.wastage_pct for i in inventory) / len(inventory), 1) if inventory else 0,
            "health_score": score
        }

    def generate_reorder_recommendations(self, inventory: List[InventoryItem], days_ahead: int = 7) -> List[Dict[str, Any]]:
        recommendations = []
        for item in inventory:
            projected_usage = item.daily_usage_avg * days_ahead
            safety_stock = item.daily_usage_avg * self.safety_stock_multiplier
            order_qty = projected_usage + safety_stock - item.current_stock

            if order_qty > 0:
                if item.stock_status == "out_of_stock":
                    priority = "critical"
                elif item.stock_status == "low":
                    priority = "high"
                elif item.days_remaining < days_ahead:
                    priority = "medium"
                else:
                    priority = "low"

                recommendations.append({
                    "item_name": item.name,
                    "item_uid": item.uid,
                    "category": item.category.value,
                    "current_stock": item.current_stock,
                    "unit": item.unit,
                    "projected_usage": round(projected_usage, 1),
                    "order_quantity": round(max(order_qty, item.min_stock), 1),
                    "estimated_cost": round(max(order_qty, item.min_stock) * item.unit_cost, 2),
                    "priority": priority,
                    "days_remaining": round(item.days_remaining, 1),
                    "supplier_uid": item.supplier_uid
                })

        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
        return recommendations

    def generate_procurement_draft(self, recommendations: List[Dict[str, Any]], suppliers: List[Supplier]) -> List[ProcurementOrder]:
        supplier_items = {}
        for rec in recommendations:
            if rec['priority'] in ['critical', 'high', 'medium']:
                cat = rec['category']
                best_supplier = None
                best_score = -1
                for supplier in suppliers:
                    cat_match = any(c.value == cat for c in supplier.categories)
                    if cat_match and supplier.is_active:
                        score = supplier.reliability_score * 0.5 + supplier.avg_fill_rate * 0.3 + (1 / max(supplier.lead_time_days, 0.5)) * 0.2
                        if score > best_score:
                            best_score = score
                            best_supplier = supplier
                if best_supplier:
                    if best_supplier.uid not in supplier_items:
                        supplier_items[best_supplier.uid] = {"supplier": best_supplier, "items": []}
                    supplier_items[best_supplier.uid]["items"].append(rec)

        orders = []
        for supplier_uid, data in supplier_items.items():
            supplier = data["supplier"]
            items = data["items"]
            order_items = []
            total_value = 0
            for item in items:
                order_items.append({
                    "item_name": item["item_name"],
                    "quantity": item["order_quantity"],
                    "unit": item["unit"],
                    "unit_cost": item["estimated_cost"] / item["order_quantity"] if item["order_quantity"] > 0 else 0,
                    "total": item["estimated_cost"]
                })
                total_value += item["estimated_cost"]
            order = ProcurementOrder(
                supplier_uid=supplier_uid,
                items=order_items,
                total_value=round(total_value, 2),
                expected_delivery=datetime.now() + timedelta(days=supplier.lead_time_days),
                status="draft",
                auto_generated=True
            )
            orders.append(order)
        return orders

    def calculate_waste_metrics(self, inventory: List[InventoryItem]) -> Dict[str, Any]:
        if not inventory:
            return {}
        total_waste_cost = 0
        high_waste_items = []
        for item in inventory:
            waste_cost = item.current_stock * item.unit_cost * (item.wastage_pct / 100)
            total_waste_cost += waste_cost
            if item.wastage_pct > 8:
                high_waste_items.append({
                    "name": item.name,
                    "wastage_pct": item.wastage_pct,
                    "waste_cost": round(waste_cost, 2),
                    "category": item.category.value
                })
        high_waste_items.sort(key=lambda x: x['waste_cost'], reverse=True)

        cat_waste = {}
        cat_count = {}
        for item in inventory:
            cat = item.category.value
            cat_waste[cat] = cat_waste.get(cat, 0) + item.wastage_pct
            cat_count[cat] = cat_count.get(cat, 0) + 1

        return {
            "total_waste_cost_monthly": round(total_waste_cost * 4, 2),
            "avg_wastage_pct": round(sum(i.wastage_pct for i in inventory) / len(inventory), 1),
            "high_waste_items": high_waste_items,
            "potential_savings": round(total_waste_cost * 4 * 0.4, 2),
            "waste_by_category": {cat: round(cat_waste[cat] / cat_count[cat], 1) for cat in cat_waste}
        }
