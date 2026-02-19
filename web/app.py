"""
Forkast Platform - Web GUI
Prediction-first AI platform for MENA restaurants
"""
import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

st.set_page_config(
    page_title="Forkast - AI Restaurant Platform",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Premium CSS Theme ---
st.markdown("""
<style>
    /* ---- Global ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 0.5rem; padding-bottom: 2rem; }

    /* ---- Hide sidebar ---- */
    [data-testid="stSidebar"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="stSidebarCollapsedControl"] { display: none !important; }

    /* ---- Header styles ---- */
    .main-header {
        font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header { font-size: 1.3rem; color: #636e72; font-weight: 400; margin-bottom: 1.5rem; }
    .page-desc { color: #636e72; font-size: 0.95rem; margin-bottom: 1.5rem; }

    /* ---- KPI Cards ---- */
    .kpi-card {
        background: white; border-radius: 16px; padding: 1.4rem 1.2rem;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
    .kpi-icon { width: 48px; height: 48px; border-radius: 12px; display: flex;
        align-items: center; justify-content: center; margin-bottom: 0.8rem; font-size: 1.4rem; }
    .kpi-icon-orange { background: rgba(255,107,53,0.12); color: #FF6B35; }
    .kpi-icon-green { background: rgba(40,167,69,0.12); color: #28a745; }
    .kpi-icon-red { background: rgba(220,53,69,0.12); color: #dc3545; }
    .kpi-icon-blue { background: rgba(23,162,184,0.12); color: #17a2b8; }
    .kpi-icon-purple { background: rgba(111,66,193,0.12); color: #6f42c1; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; color: #2D3436; line-height: 1.2; }
    .kpi-label { font-size: 0.8rem; color: #636e72; font-weight: 500; text-transform: uppercase;
        letter-spacing: 0.5px; margin-top: 0.3rem; }
    .kpi-delta { font-size: 0.85rem; font-weight: 600; margin-top: 0.2rem; }
    .kpi-delta-up { color: #28a745; }
    .kpi-delta-down { color: #dc3545; }

    /* ---- Cards & Sections ---- */
    .section-card {
        background: white; border-radius: 16px; padding: 1.5rem;
        border: 1px solid #f0f0f0; box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #2D3436;
        margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
    }
    .section-title::before {
        content: ''; width: 4px; height: 24px; border-radius: 2px;
        background: linear-gradient(180deg, #FF6B35, #F7931E); display: inline-block;
    }
    .insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 12px; padding: 1.2rem; border-left: 4px solid #FF6B35;
        margin-bottom: 0.8rem; transition: transform 0.2s ease;
    }
    .insight-card:hover { transform: translateX(4px); }
    .insight-title { font-weight: 700; color: #2D3436; font-size: 0.95rem; }
    .insight-desc { color: #636e72; font-size: 0.85rem; margin-top: 0.3rem; }

    /* ---- Alert styles ---- */
    .alert-critical {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        padding: 1rem 1.2rem; border-radius: 12px; border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .alert-high {
        background: linear-gradient(135deg, #fffbf0 0%, #ffeaa7 100%);
        padding: 1rem 1.2rem; border-radius: 12px; border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background: linear-gradient(135deg, #f0f9ff 0%, #bee3f8 100%);
        padding: 1rem 1.2rem; border-radius: 12px; border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
    .alert-low {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        padding: 1rem 1.2rem; border-radius: 12px; border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }

    /* ---- Top Navigation Bar ---- */
    .nav-bar {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px; padding: 0.6rem 1.2rem; margin-bottom: 0.5rem;
    }
    .nav-restaurant {
        text-align: right; padding: 0.2rem 0;
    }
    .nav-restaurant-name {
        font-size: 0.85rem; font-weight: 700; color: #FF6B35;
    }
    .nav-restaurant-loc {
        font-size: 0.7rem; color: #a0a0a0;
    }

    /* ---- Status strip ---- */
    .status-strip {
        display: flex; align-items: center; gap: 0.8rem;
        flex-wrap: wrap; padding: 0.3rem 0;
    }
    .status-item {
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.35rem 0.9rem; background: white; border-radius: 20px;
        font-size: 0.8rem; font-weight: 600; border: 1px solid #f0f0f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        color: #2D3436;
    }
    .status-value { color: #FF6B35; font-weight: 700; }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 2px solid #f0f0f0; }
    .stTabs [data-baseweb="tab"] {
        height: 48px; padding: 0 1.5rem; border-radius: 8px 8px 0 0;
        font-weight: 600; font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%) !important;
        color: white !important;
    }

    /* ---- Tables ---- */
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #f0f0f0; }

    /* ---- Metric tweaks ---- */
    [data-testid="stMetricValue"] { font-weight: 800; }
    [data-testid="stMetricDelta"] { font-weight: 600; }

    /* ---- Plotly chart containers ---- */
    .js-plotly-plot { border-radius: 12px; }

    /* ---- Hero Banner ---- */
    .hero-banner { margin-bottom: 1.5rem; }
    .hero-banner img { border-radius: 16px; }

    /* ---- Status badges ---- */
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600; }
    .badge-critical { background: #dc3545; color: white; }
    .badge-high { background: #ffc107; color: #2D3436; }
    .badge-medium { background: #17a2b8; color: white; }
    .badge-low { background: #28a745; color: white; }
    .badge-normal { background: #28a745; color: white; }
    .badge-warning { background: #ffc107; color: #2D3436; }
    .badge-danger { background: #dc3545; color: white; }

    /* ---- Procurement cards ---- */
    .po-card {
        background: white; border-radius: 12px; padding: 1.2rem;
        border: 1px solid #e9ecef; margin-bottom: 0.8rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    /* ---- Gauge container ---- */
    .gauge-container { text-align: center; padding: 0.5rem; }

    /* ---- Footer ---- */
    .app-footer {
        text-align: center; padding: 1rem 0; margin-top: 2rem;
        border-top: 1px solid #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with demo data
if 'initialized' not in st.session_state:
    from data.demo_generator import DemoDataGenerator
    from forecasting.demand_engine import DemandForecastEngine

    gen = DemoDataGenerator()
    data = gen.generate_all()

    st.session_state.restaurant = data['restaurant']
    st.session_state.menu = data['menu']
    st.session_state.inventory = data['inventory']
    st.session_state.suppliers = data['suppliers']
    st.session_state.historical_orders = data['historical_orders']
    st.session_state.alerts = data['alerts']
    st.session_state.staff_schedule = data['staff_schedule']

    # Train forecast engine
    engine = DemandForecastEngine()
    engine.train(data['historical_orders'])
    st.session_state.forecast_engine = engine
    st.session_state.forecasts = engine.forecast(days_ahead=14)
    st.session_state.insights = engine.get_insights()

    st.session_state.initialized = True

# --- Imports ---
from web.assets.images import SIDEBAR_LOGO_SVG, render_svg, health_gauge_svg
from web.utils.currency import CURRENCIES

# --- Navigation Data ---
NAV_GROUPS = {
    "Operations": [
        "Demand Forecast", "Inventory", "Procurement",
        "Menu Optimization", "Labor Scheduling",
    ],
    "Network": [
        "Suppliers", "Payment Gateway", "Loyalty Program",
    ],
    "Intelligence": [
        "Analytics", "Alerts", "Revenue Model",
    ],
    "Admin": [
        "API Management", "Register Restaurant",
        "Register Supplier", "Settings",
    ],
}

NAV_ICONS = {
    "Operations": "⚙️",
    "Network": "🔗",
    "Intelligence": "📊",
    "Admin": "🛠️",
}

# Map page names to their group for active-group indication
PAGE_TO_GROUP = {}
for grp, pages in NAV_GROUPS.items():
    for p in pages:
        PAGE_TO_GROUP[p] = grp

# Initialize navigation state
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"

# Currency setup
currency_codes = list(CURRENCIES.keys())
currency_labels_map = {k: f"{v['flag']} {k} - {v['name']}" for k, v in CURRENCIES.items()}
_cur = st.session_state.get("currency", "AED")
_idx = currency_codes.index(_cur) if _cur in currency_codes else 0

# ============================================================
# TOP NAVIGATION BAR
# ============================================================
# Dark header bar with logo and restaurant info
st.markdown(
    f'<div class="nav-bar">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
    f'<div>{render_svg(SIDEBAR_LOGO_SVG, width="150px")}</div>'
    f'<div class="nav-restaurant">'
    f'<div class="nav-restaurant-name">{st.session_state.restaurant.name}</div>'
    f'<div class="nav-restaurant-loc">📍 {st.session_state.restaurant.city}, {st.session_state.restaurant.country}</div>'
    f'</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Navigation row: Dashboard button + 4 group dropdowns + Currency selector
nav_cols = st.columns([1.2, 1.5, 1.5, 1.5, 1.5, 1.5])

with nav_cols[0]:
    active_page = st.session_state.nav_page
    dash_label = "🏠 Dashboard" if active_page == "Dashboard" else "🏠 Dashboard"
    dash_type = "primary" if active_page == "Dashboard" else "secondary"
    if st.button(dash_label, use_container_width=True, type=dash_type):
        st.session_state.nav_page = "Dashboard"
        st.rerun()

for idx, (group_name, pages) in enumerate(NAV_GROUPS.items()):
    with nav_cols[idx + 1]:
        icon = NAV_ICONS.get(group_name, "")
        # Show active indicator if current page is in this group
        is_active = active_page in pages
        display_label = f"{icon} {group_name}"
        if is_active:
            display_label = f"● {icon} {group_name}"

        # Build options: empty string (shows group name) + page names
        options = [""] + pages
        key = f"nav_{group_name}"

        # Capture pending selection BEFORE widget creation, then reset
        if key in st.session_state and st.session_state[key] != "":
            st.session_state.nav_page = st.session_state[key]
            del st.session_state[key]
            st.rerun()

        st.selectbox(
            display_label,
            options=options,
            index=0,
            format_func=lambda x, lbl=display_label: lbl if x == "" else f"  {x}",
            key=key,
            label_visibility="collapsed",
        )

with nav_cols[5]:
    _selected = st.selectbox(
        "Currency",
        currency_codes,
        index=_idx,
        format_func=lambda x: f"💱 {currency_labels_map[x]}",
        label_visibility="collapsed",
    )
    st.session_state.currency = _selected

# ============================================================
# STATUS STRIP - Metrics bar
# ============================================================
unread = sum(1 for a in st.session_state.alerts if not a.is_read)
accuracy = st.session_state.forecast_engine.accuracy_metrics.get('accuracy', 0)

health = 0
if st.session_state.inventory:
    from inventory.optimizer import InventoryOptimizer
    opt = InventoryOptimizer()
    analysis = opt.analyze_inventory(st.session_state.inventory)
    health = analysis['health_score']

sc1, sc2, sc3, sc4 = st.columns([3, 3, 3, 2])
with sc1:
    st.markdown(
        f'<div class="status-item">🔔 <span class="status-value">{unread}</span> Alerts</div>',
        unsafe_allow_html=True,
    )
with sc2:
    st.markdown(
        f'<div class="status-item">🎯 Forecast: <span class="status-value">{accuracy}%</span></div>',
        unsafe_allow_html=True,
    )
with sc3:
    st.markdown(
        f'<div class="status-item">📦 Health: <span class="status-value">{health}/100</span></div>',
        unsafe_allow_html=True,
    )
with sc4:
    st.markdown(render_svg(health_gauge_svg(health), width="60px"), unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.nav_page

if page == "Dashboard":
    from web.pages import dashboard
    dashboard.show()
elif page == "Demand Forecast":
    from web.pages import forecast_page
    forecast_page.show()
elif page == "Inventory":
    from web.pages import inventory_page
    inventory_page.show()
elif page == "Procurement":
    from web.pages import procurement_page
    procurement_page.show()
elif page == "Menu Optimization":
    from web.pages import menu_page
    menu_page.show()
elif page == "Labor Scheduling":
    from web.pages import labor_page
    labor_page.show()
elif page == "Suppliers":
    from web.pages import suppliers_page
    suppliers_page.show()
elif page == "Analytics":
    from web.pages import analytics_page
    analytics_page.show()
elif page == "Alerts":
    from web.pages import alerts_page
    alerts_page.show()
elif page == "Payment Gateway":
    from web.pages import payment_gateway_page
    payment_gateway_page.show()
elif page == "Revenue Model":
    from web.pages import revenue_model_page
    revenue_model_page.show()
elif page == "Loyalty Program":
    from web.pages import loyalty_page
    loyalty_page.show()
elif page == "API Management":
    from web.pages import api_management_page
    api_management_page.show()
elif page == "Register Restaurant":
    from web.pages import register_restaurant_page
    register_restaurant_page.show()
elif page == "Register Supplier":
    from web.pages import register_supplier_page
    register_supplier_page.show()
elif page == "Settings":
    from web.pages import settings_page
    settings_page.show()

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="app-footer">'
    '<div style="font-size:0.75rem;color:#636e72;">Forkast v1.0 | MENA Edition</div>'
    '<div style="font-size:0.7rem;color:#a0a0a0;">Prediction-first AI Platform</div>'
    '</div>', unsafe_allow_html=True
)
