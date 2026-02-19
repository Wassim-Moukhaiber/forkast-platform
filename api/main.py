"""
Forkast API - FastAPI Application
Main entry point for the REST API server
"""
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.config import settings
from api.database import create_tables, SessionLocal
from api.routers import health, pos, payments, loyalty


def seed_database():
    """Seed the database with demo data if empty."""
    from api.models.db_models import RestaurantDB, MenuItemDB, InventoryItemDB, SupplierDB
    db = SessionLocal()
    try:
        if db.query(RestaurantDB).count() > 0:
            return

        from data.demo_generator import DemoDataGenerator
        gen = DemoDataGenerator()
        data = gen.generate_all()

        # Seed restaurant
        rest = data["restaurant"]
        db_rest = RestaurantDB(
            uid=rest.uid, name=rest.name,
            restaurant_type=rest.restaurant_type.value,
            cuisine=rest.cuisine.value,
            city=rest.city, country=rest.country,
            seats=rest.seats, avg_daily_covers=rest.avg_daily_covers,
            monthly_revenue=rest.monthly_revenue,
            operating_hours=rest.operating_hours,
            staff_count=rest.staff_count,
        )
        db.add(db_rest)

        # Seed menu
        for item in data["menu"]:
            db.add(MenuItemDB(
                uid=item.uid, restaurant_uid=rest.uid,
                name=item.name, category=item.category,
                price=item.price, cost=item.cost,
                prep_time_minutes=item.prep_time_minutes,
                ingredients=item.ingredients,
                is_active=item.is_active,
                popularity_score=item.popularity_score,
                avg_daily_orders=item.avg_daily_orders,
                food_cost_pct=item.food_cost_pct,
            ))

        # Seed inventory
        for inv in data["inventory"]:
            db.add(InventoryItemDB(
                uid=inv.uid, restaurant_uid=rest.uid,
                name=inv.name, category=inv.category.value,
                unit=inv.unit, current_stock=inv.current_stock,
                min_stock=inv.min_stock, max_stock=inv.max_stock,
                reorder_point=inv.reorder_point, unit_cost=inv.unit_cost,
                shelf_life_days=inv.shelf_life_days,
                supplier_uid=inv.supplier_uid,
                daily_usage_avg=inv.daily_usage_avg,
                wastage_pct=inv.wastage_pct,
            ))

        # Seed suppliers
        for sup in data["suppliers"]:
            db.add(SupplierDB(
                uid=sup.uid, name=sup.name,
                tier=sup.tier.value,
                categories=[c.value for c in sup.categories],
                city=sup.city, country=sup.country,
                lead_time_days=sup.lead_time_days,
                min_order_value=sup.min_order_value,
                reliability_score=sup.reliability_score,
                avg_fill_rate=sup.avg_fill_rate,
                contact_email=sup.contact_email,
                contact_phone=sup.contact_phone,
                is_active=sup.is_active,
                total_orders=sup.total_orders,
                total_value=sup.total_value,
            ))

        db.commit()
        print(f"Database seeded: 1 restaurant, {len(data['menu'])} menu items, "
              f"{len(data['inventory'])} inventory items, {len(data['suppliers'])} suppliers")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    create_tables()
    seed_database()
    print(f"Forkast API v{settings.app_version} started on port {settings.api_port}")
    print(f"Swagger docs: http://localhost:{settings.api_port}/docs")
    yield
    print("Forkast API shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for Forkast - AI Restaurant Platform for MENA. "
                "Provides POS integration, payment gateway, and data sync endpoints.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(pos.router)
app.include_router(payments.router)
app.include_router(loyalty.router)


@app.get("/", include_in_schema=False)
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.debug,
    )
