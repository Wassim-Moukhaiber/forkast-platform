"""Register Restaurant Page"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import REGISTER_RESTAURANT_HEADER_SVG, render_svg
from models.core import Restaurant, RestaurantType, CuisineType


def show():
    st.markdown(render_svg(REGISTER_RESTAURANT_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Register your restaurant to unlock AI-powered demand forecasting, '
        'inventory optimization, and operational insights.</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Restaurant Details</div>', unsafe_allow_html=True)

    with st.form("register_restaurant", clear_on_submit=False):
        # Row 1: Name, Type, Cuisine
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Restaurant Name *")
        with c2:
            rest_type = st.selectbox(
                "Restaurant Type *",
                options=[t for t in RestaurantType],
                format_func=lambda t: t.value.replace("_", " ").title(),
            )
        with c3:
            cuisine = st.selectbox(
                "Cuisine *",
                options=[c for c in CuisineType],
                format_func=lambda c: c.value.title(),
            )

        # Row 2: City, Country, Operating Hours
        c1, c2, c3 = st.columns(3)
        with c1:
            city = st.text_input("City *", value="Dubai")
        with c2:
            country = st.text_input("Country", value="UAE")
        with c3:
            operating_hours = st.text_input("Operating Hours", value="10:00-23:00")

        # Row 3: Seats, Avg Covers, Monthly Revenue, Staff
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            seats = st.number_input("Seats", min_value=1, value=40)
        with c2:
            avg_covers = st.number_input("Avg Daily Covers", min_value=1, value=80)
        with c3:
            monthly_rev = st.number_input("Monthly Revenue (AED)", min_value=0.0, value=50000.0, step=1000.0)
        with c4:
            staff_count = st.number_input("Staff Count", min_value=1, value=10)

        submitted = st.form_submit_button("Register Restaurant", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        # Validation
        if not name.strip():
            st.error("Restaurant name is required.")
            return
        if not city.strip():
            st.error("City is required.")
            return

        restaurant = Restaurant(
            name=name.strip(),
            restaurant_type=rest_type,
            cuisine=cuisine,
            city=city.strip(),
            country=country.strip() or "UAE",
            seats=seats,
            avg_daily_covers=avg_covers,
            monthly_revenue=monthly_rev,
            operating_hours=operating_hours.strip(),
            staff_count=staff_count,
        )

        # Store and regenerate platform data
        st.session_state.restaurant = restaurant

        from data.demo_generator import DemoDataGenerator
        from forecasting.demand_engine import DemandForecastEngine

        gen = DemoDataGenerator()
        data = gen.generate_all()

        # Keep the new restaurant but refresh operational data
        st.session_state.menu = data['menu']
        st.session_state.inventory = data['inventory']
        st.session_state.suppliers = data['suppliers']
        st.session_state.historical_orders = data['historical_orders']
        st.session_state.alerts = data['alerts']
        st.session_state.staff_schedule = data['staff_schedule']

        engine = DemandForecastEngine()
        engine.train(data['historical_orders'])
        st.session_state.forecast_engine = engine
        st.session_state.forecasts = engine.forecast(days_ahead=14)
        st.session_state.insights = engine.get_insights()

        st.success(f"Restaurant **{restaurant.name}** registered successfully!")

        # Summary card
        st.markdown(
            f'<div class="section-card">'
            f'<div class="section-title">Registration Summary</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;">'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Name</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.name}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Type</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.restaurant_type.value.replace("_"," ").title()}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Cuisine</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.cuisine.value.title()}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Location</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.city}, {restaurant.country}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Seats</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.seats}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Avg Daily Covers</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.avg_daily_covers}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Staff</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.staff_count}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Hours</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{restaurant.operating_hours}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
