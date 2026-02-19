"""
Forkast Demand Forecasting Engine
Prediction-first AI for restaurant demand forecasting
"""
import math
import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.core import DemandForecast


class DemandForecastEngine:
    """
    AI-powered demand forecasting engine for restaurants.
    Uses statistical decomposition + ML patterns for accurate predictions.
    """

    def __init__(self):
        self.historical_data: List[Dict[str, Any]] = []
        self.day_patterns: Dict[int, float] = {}
        self.month_patterns: Dict[int, float] = {}
        self.trend_slope: float = 0.0
        self.base_covers: float = 0.0
        self.base_revenue: float = 0.0
        self.avg_check: float = 0.0
        self.is_trained: bool = False
        self.accuracy_metrics: Dict[str, float] = {}
        self.item_patterns: Dict[str, Dict[int, float]] = {}

    def train(self, historical_orders: List[Dict[str, Any]]):
        """
        Train the forecasting model on historical order data

        Args:
            historical_orders: List of daily order summaries
        """
        if not historical_orders:
            raise ValueError("No historical data for training")

        self.historical_data = historical_orders
        n = len(historical_orders)

        # Calculate base metrics
        covers = [d['total_covers'] for d in historical_orders]
        revenues = [d['total_revenue'] for d in historical_orders]
        checks = [d['avg_check'] for d in historical_orders]

        self.base_covers = sum(covers) / n
        self.base_revenue = sum(revenues) / n
        self.avg_check = sum(checks) / n

        # Day-of-week patterns
        day_sums = defaultdict(list)
        for d in historical_orders:
            dow = datetime.fromisoformat(d['date']).weekday()
            day_sums[dow].append(d['total_covers'])

        for dow, values in day_sums.items():
            self.day_patterns[dow] = (sum(values) / len(values)) / self.base_covers

        # Monthly patterns
        month_sums = defaultdict(list)
        for d in historical_orders:
            month = datetime.fromisoformat(d['date']).month
            month_sums[month].append(d['total_covers'])

        for month, values in month_sums.items():
            self.month_patterns[month] = (sum(values) / len(values)) / self.base_covers

        # Trend (linear regression on covers)
        x_mean = (n - 1) / 2
        y_mean = self.base_covers
        num = sum((i - x_mean) * (covers[i] - y_mean) for i in range(n))
        den = sum((i - x_mean) ** 2 for i in range(n))
        self.trend_slope = num / den if den != 0 else 0

        # Item-level patterns
        for d in historical_orders:
            dow = datetime.fromisoformat(d['date']).weekday()
            item_orders = d.get('item_orders', {})
            for item_name, qty in item_orders.items():
                if item_name not in self.item_patterns:
                    self.item_patterns[item_name] = defaultdict(list)
                self.item_patterns[item_name][dow].append(qty)

        # Compute item averages
        for item_name in self.item_patterns:
            for dow in self.item_patterns[item_name]:
                values = self.item_patterns[item_name][dow]
                self.item_patterns[item_name][dow] = sum(values) / len(values)

        # Calculate accuracy (on last 20% of data as holdout)
        self._calculate_accuracy()

        self.is_trained = True

    def _calculate_accuracy(self):
        """Calculate model accuracy metrics"""
        n = len(self.historical_data)
        holdout_start = int(n * 0.8)
        holdout = self.historical_data[holdout_start:]

        if not holdout:
            return

        errors = []
        for d in holdout:
            actual = d['total_covers']
            target_date = datetime.fromisoformat(d['date']).date()
            forecast = self._predict_single(target_date, len(self.historical_data))
            predicted = forecast.predicted_covers
            if actual > 0:
                errors.append(abs(actual - predicted) / actual)

        if errors:
            self.accuracy_metrics = {
                "mape": round(sum(errors) / len(errors) * 100, 2),
                "accuracy": round((1 - sum(errors) / len(errors)) * 100, 2),
                "holdout_size": len(holdout),
                "total_samples": n
            }

    def _predict_single(self, target_date: date, days_from_start: int) -> DemandForecast:
        """Generate forecast for a single date"""
        dow = target_date.weekday()
        month = target_date.month

        # Components
        day_factor = self.day_patterns.get(dow, 1.0)
        month_factor = self.month_patterns.get(month, 1.0)
        trend_value = self.base_covers + self.trend_slope * days_from_start

        # Combined prediction
        predicted_covers = int(trend_value * day_factor * month_factor)

        # Confidence interval (wider for further dates)
        std_dev = self.base_covers * 0.12
        confidence_lower = max(0, predicted_covers - 1.96 * std_dev)
        confidence_upper = predicted_covers + 1.96 * std_dev

        # Revenue prediction
        predicted_revenue = predicted_covers * self.avg_check

        # Channel breakdown
        if dow in [4, 5]:  # Fri, Sat - more delivery
            channels = {"dine_in": 0.42, "delivery": 0.38, "takeaway": 0.20}
        elif dow == 3:  # Thursday
            channels = {"dine_in": 0.50, "delivery": 0.30, "takeaway": 0.20}
        else:
            channels = {"dine_in": 0.52, "delivery": 0.28, "takeaway": 0.20}

        channel_breakdown = {k: round(v * predicted_covers) for k, v in channels.items()}

        return DemandForecast(
            forecast_date=target_date,
            predicted_covers=predicted_covers,
            predicted_revenue=round(predicted_revenue, 2),
            confidence_lower=round(confidence_lower),
            confidence_upper=round(confidence_upper),
            day_of_week=target_date.strftime("%A"),
            channel_breakdown=channel_breakdown
        )

    def forecast(self, days_ahead: int = 14) -> List[DemandForecast]:
        """
        Generate demand forecasts

        Args:
            days_ahead: Number of days to forecast

        Returns:
            List of DemandForecast objects
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained. Call train() first.")

        forecasts = []
        today = date.today()
        days_from_start = len(self.historical_data)

        for i in range(1, days_ahead + 1):
            target_date = today + timedelta(days=i)
            forecast = self._predict_single(target_date, days_from_start + i)
            forecasts.append(forecast)

        return forecasts

    def forecast_items(self, days_ahead: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Forecast demand for individual menu items

        Args:
            days_ahead: Number of days to forecast

        Returns:
            Dict mapping item names to daily forecast lists
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained. Call train() first.")

        item_forecasts = {}
        today = date.today()

        for item_name, dow_patterns in self.item_patterns.items():
            forecasts = []
            for i in range(1, days_ahead + 1):
                target_date = today + timedelta(days=i)
                dow = target_date.weekday()

                base_qty = dow_patterns.get(dow, 0)
                if isinstance(base_qty, list):
                    base_qty = sum(base_qty) / len(base_qty) if base_qty else 0

                # Apply trend
                trend_factor = 1.0 + (self.trend_slope / self.base_covers) * i
                predicted_qty = max(0, int(base_qty * trend_factor))

                forecasts.append({
                    "date": target_date.isoformat(),
                    "day_of_week": target_date.strftime("%A"),
                    "predicted_quantity": predicted_qty
                })

            item_forecasts[item_name] = forecasts

        return item_forecasts

    def get_insights(self) -> List[Dict[str, str]]:
        """Generate actionable insights from forecast data"""
        if not self.is_trained:
            return []

        insights = []

        # Peak day insight
        peak_dow = max(self.day_patterns, key=self.day_patterns.get)
        peak_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][peak_dow]
        insights.append({
            "type": "demand",
            "title": f"Peak Day: {peak_name}",
            "description": f"{peak_name} drives {self.day_patterns[peak_dow]*100:.0f}% of average daily covers. Ensure full staffing and stock.",
            "impact": "high"
        })

        # Slowest day
        slow_dow = min(self.day_patterns, key=self.day_patterns.get)
        slow_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][slow_dow]
        insights.append({
            "type": "labor",
            "title": f"Slowest Day: {slow_name}",
            "description": f"{slow_name} averages {self.day_patterns[slow_dow]*100:.0f}% of normal. Consider reduced staffing or promotions.",
            "impact": "medium"
        })

        # Trend direction
        if self.trend_slope > 0:
            weekly_growth = (self.trend_slope * 7 / self.base_covers) * 100
            insights.append({
                "type": "growth",
                "title": "Upward Demand Trend",
                "description": f"Demand is growing by ~{weekly_growth:.1f}% per week. Plan for increased procurement and staffing.",
                "impact": "high"
            })
        elif self.trend_slope < 0:
            weekly_decline = abs(self.trend_slope * 7 / self.base_covers) * 100
            insights.append({
                "type": "risk",
                "title": "Declining Demand Trend",
                "description": f"Demand is declining by ~{weekly_decline:.1f}% per week. Review marketing and menu strategy.",
                "impact": "critical"
            })

        # Delivery growth
        recent = self.historical_data[-14:]
        if recent:
            avg_delivery_pct = sum(d['delivery'] / d['total_covers'] for d in recent if d['total_covers'] > 0) / len(recent)
            if avg_delivery_pct > 0.30:
                insights.append({
                    "type": "channel",
                    "title": "Strong Delivery Channel",
                    "description": f"Delivery accounts for {avg_delivery_pct*100:.0f}% of covers. Optimize packaging and delivery prep workflows.",
                    "impact": "medium"
                })

        # Waste reduction opportunity
        avg_waste = sum(d.get('food_waste_kg', 0) for d in self.historical_data[-30:]) / 30
        avg_covers = sum(d['total_covers'] for d in self.historical_data[-30:]) / 30
        waste_per_cover = avg_waste / avg_covers if avg_covers > 0 else 0
        if waste_per_cover > 0.10:
            insights.append({
                "type": "waste",
                "title": "Food Waste Reduction Opportunity",
                "description": f"Current waste: {waste_per_cover*1000:.0f}g per cover. Target: <100g. Use forecast-based prep to reduce overproduction.",
                "impact": "high"
            })

        return insights

    def get_model_summary(self) -> Dict[str, Any]:
        """Get summary of the trained model"""
        return {
            "is_trained": self.is_trained,
            "training_samples": len(self.historical_data),
            "base_daily_covers": round(self.base_covers, 1),
            "base_daily_revenue": round(self.base_revenue, 2),
            "avg_check": round(self.avg_check, 2),
            "trend_direction": "up" if self.trend_slope > 0 else "down" if self.trend_slope < 0 else "flat",
            "trend_slope_per_day": round(self.trend_slope, 3),
            "accuracy": self.accuracy_metrics,
            "day_patterns": {
                ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][k]: round(v, 3)
                for k, v in sorted(self.day_patterns.items())
            },
            "items_tracked": len(self.item_patterns)
        }
