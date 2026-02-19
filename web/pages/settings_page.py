"""Settings Page - Enhanced"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import (
    LOGO_SVG, render_svg, SETTINGS_HEADER_SVG,
    MODULE_GATING_SVG, PLATFORM_ARCHITECTURE_SVG, NETWORK_EFFECTS_SVG
)


def show():
    st.markdown(render_svg(SETTINGS_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">Configure your restaurant profile, AI settings, and platform preferences.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Restaurant Profile", "AI Configuration", "About Forkast"])

    with tab1:
        rest = st.session_state.restaurant

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Restaurant Profile</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Restaurant Name", value=rest.name, disabled=True)
            st.text_input("City", value=rest.city, disabled=True)
            st.text_input("Type", value=rest.restaurant_type.value.replace("_", " ").title(), disabled=True)
        with col2:
            st.text_input("Cuisine", value=rest.cuisine.value.title(), disabled=True)
            st.number_input("Seats", value=rest.seats, disabled=True)
            st.number_input("Staff Count", value=rest.staff_count, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Configuration</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.slider("Forecast Horizon (days)", 7, 30, 14)
            st.slider("Safety Stock Multiplier", 1.0, 3.0, 1.5, 0.1)
            st.selectbox("Forecast Model", ["Forkast Ensemble (Default)", "Statistical Only", "ML Only"])
        with col2:
            st.checkbox("Enable Real-time Alerts", value=True)
            st.checkbox("Auto-generate Procurement Drafts", value=True)
            st.checkbox("Human-in-the-Loop for all decisions", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="alert-medium">'
            '<strong>Governance</strong><br>'
            'All AI actions require human approval before execution. '
            'The Human-in-the-Loop setting ensures transparency and control.'
            '</div>',
            unsafe_allow_html=True
        )

    with tab3:
        # Logo
        st.markdown(render_svg(LOGO_SVG, width="300px"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">About Forkast</div>', unsafe_allow_html=True)

        st.markdown(
            '<div style="padding:0.5rem 0;">'
            '<div style="font-weight:700;font-size:1.1rem;color:#2D3436;">Forkast v1.0</div>'
            '<div style="color:#636e72;">Prediction-First AI Platform for MENA Restaurants</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Mission
        st.markdown(
            '<div class="insight-card">'
            '<div class="insight-title">Mission</div>'
            '<div class="insight-desc">Resolve structural coordination failures in small and mid-sized restaurants '
            'through prediction-first, agentic AI that forecasts demand, generates interpretable insights, '
            'and executes recommendations under human oversight.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Platform Sides
        col1, col2, col3 = st.columns(3)
        sides = [
            ("kpi-icon-orange", "🏪", "Restaurants", "Core users and data contributors"),
            ("kpi-icon-blue", "🏭", "Suppliers", "Sellers with demand visibility"),
            ("kpi-icon-purple", "💻", "Tech Partners", "POS, IoT, cloud integrations"),
        ]
        for col, (icon_cls, emoji, title, desc) in zip([col1, col2, col3], sides):
            with col:
                st.markdown(f'''<div class="kpi-card" style="text-align:center;">
                    <div class="kpi-icon {icon_cls}" style="margin:0 auto 0.5rem auto;">{emoji}</div>
                    <div style="font-weight:700;color:#2D3436;">{title}</div>
                    <div style="font-size:0.8rem;color:#636e72;">{desc}</div>
                </div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Core capabilities
        st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)
        capabilities = [
            "Demand forecasting with explainable AI",
            "Inventory optimization and waste reduction",
            "Smart procurement with auto-generated drafts",
            "Menu engineering and profitability analysis",
            "Labor scheduling aligned to demand",
            "Supplier performance management",
            "Growth analytics and CLV modeling",
        ]
        for cap in capabilities:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.8rem;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
                f'<div style="width:8px;height:8px;border-radius:50%;background:#FF6B35;flex-shrink:0;"></div>'
                f'<span style="color:#2D3436;">{cap}</span></div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Key differentiators
        st.markdown('<div class="section-title">Key Differentiators</div>', unsafe_allow_html=True)
        diffs = [
            ("Prediction-First", "Not just analytics - actionable forecasts that drive decisions"),
            ("Human-in-the-Loop", "AI recommends, humans approve - full transparency"),
            ("MENA-Localized", "Cuisine patterns, calendar, suppliers tuned for the region"),
            ("Multi-Sided Platform", "Network effects between restaurants, suppliers, and tech partners"),
            ("Explainable AI", "Clear reasoning for non-technical restaurant operators"),
        ]
        for title, desc in diffs:
            st.markdown(
                f'<div class="insight-card">'
                f'<div class="insight-title">{title}</div>'
                f'<div class="insight-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # --- Platform Architecture Diagram ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Platform Architecture</div>', unsafe_allow_html=True)
        st.markdown(render_svg(PLATFORM_ARCHITECTURE_SVG, width="100%"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Module Gating Table ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Module Access Tiers</div>', unsafe_allow_html=True)
        st.markdown(render_svg(MODULE_GATING_SVG, width="100%"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Network Effects Diagram ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Network Effects</div>', unsafe_allow_html=True)
        st.markdown(render_svg(NETWORK_EFFECTS_SVG, width="100%"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center;padding:1.5rem 0;color:#636e72;font-size:0.85rem;">'
            'Built for the MENA Food Service Industry</div>',
            unsafe_allow_html=True
        )
