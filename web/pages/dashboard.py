"""Dashboard Page - Enhanced with visuals"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import (
    HERO_SVG, render_svg, health_gauge_svg,
    PLATFORM_ARCHITECTURE_SVG, DATA_FLOW_ARCHITECTURE_SVG
)
from web.utils.currency import fmt, fmt_rate, currency_label, convert


def show():
    # Hero Banner
    st.markdown(f'<div class="hero-banner">{render_svg(HERO_SVG, width="100%")}</div>', unsafe_allow_html=True)

    rest = st.session_state.restaurant

    # --- KPI Row with custom cards ---
    orders = st.session_state.historical_orders
    last_7 = orders[-7:]
    prev_7 = orders[-14:-7]

    avg_covers = sum(d['total_covers'] for d in last_7) / 7
    prev_covers = sum(d['total_covers'] for d in prev_7) / 7
    covers_delta = ((avg_covers - prev_covers) / prev_covers * 100) if prev_covers > 0 else 0

    avg_revenue = sum(d['total_revenue'] for d in last_7) / 7
    prev_revenue = sum(d['total_revenue'] for d in prev_7) / 7
    rev_delta = ((avg_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0

    avg_waste = sum(d.get('food_waste_kg', 0) for d in last_7) / 7
    avg_food_cost = sum(d.get('food_cost_pct', 30) for d in last_7) / 7
    accuracy = st.session_state.forecast_engine.accuracy_metrics.get('accuracy', 0)

    from inventory.optimizer import InventoryOptimizer
    opt = InventoryOptimizer()
    inv_analysis = opt.analyze_inventory(st.session_state.inventory)
    health = inv_analysis['health_score']

    col1, col2, col3, col4, col5 = st.columns(5)

    def kpi_html(icon_class, icon_emoji, value, label, delta=None, delta_up=True):
        delta_html = ""
        if delta is not None:
            cls = "kpi-delta-up" if delta_up else "kpi-delta-down"
            arrow = "▲" if delta_up else "▼"
            delta_html = f'<div class="kpi-delta {cls}">{arrow} {abs(delta):.1f}%</div>'
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_emoji}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {delta_html}
        </div>'''

    with col1:
        st.markdown(kpi_html("kpi-icon-orange", "👥", f"{avg_covers:.0f}", "AVG DAILY COVERS",
                             covers_delta, covers_delta >= 0), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_html("kpi-icon-green", "💰", fmt(avg_revenue), "AVG DAILY REVENUE",
                             rev_delta, rev_delta >= 0), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_html("kpi-icon-blue", "📊", f"{avg_food_cost:.1f}%", "FOOD COST %"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_html("kpi-icon-red", "🗑️", f"{avg_waste:.1f} kg", "AVG FOOD WASTE"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_html("kpi-icon-purple", "🎯", f"{accuracy}%", "FORECAST ACCURACY"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Charts Row ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Revenue & Covers Trend (30 Days)</div>', unsafe_allow_html=True)
        last_30 = orders[-30:]
        dates = [d['date'] for d in last_30]
        covers = [d['total_covers'] for d in last_30]
        revenues = [d['total_revenue'] for d in last_30]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dates, y=covers, name="Covers", marker_color="#FF6B35", opacity=0.7))
        converted_rev = [convert(r) for r in revenues]
        fig.add_trace(go.Scatter(x=dates, y=[r/50 for r in converted_rev], name=f"Revenue ({currency_label()}/50)",
                                 line=dict(color="#2c3e50", width=2.5), yaxis="y"))
        fig.update_layout(
            height=350, margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", y=1.1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Channel Mix (Last 7 Days)</div>', unsafe_allow_html=True)
        total_dine = sum(d['dine_in'] for d in last_7)
        total_del = sum(d['delivery'] for d in last_7)
        total_take = sum(d['takeaway'] for d in last_7)

        fig = go.Figure(data=[go.Pie(
            labels=['Dine-in', 'Delivery', 'Takeaway'],
            values=[total_dine, total_del, total_take],
            marker_colors=['#FF6B35', '#1a1a2e', '#636e72'],
            hole=0.5,
            textinfo='label+percent', textfont=dict(size=13)
        )])
        fig.update_layout(
            height=350, margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Forecast + Alerts Row ---
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">14-Day Demand Forecast</div>', unsafe_allow_html=True)
        forecasts = st.session_state.forecasts
        fc_dates = [f.forecast_date.isoformat() for f in forecasts]
        fc_covers = [f.predicted_covers for f in forecasts]
        fc_lower = [f.confidence_lower for f in forecasts]
        fc_upper = [f.confidence_upper for f in forecasts]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fc_dates, y=fc_upper, fill=None, mode='lines',
                                 line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=fc_dates, y=fc_lower, fill='tonexty', mode='lines',
                                 line=dict(width=0), fillcolor='rgba(255,107,53,0.12)', name='Confidence Band'))
        fig.add_trace(go.Scatter(x=fc_dates, y=fc_covers, mode='lines+markers',
                                 name='Predicted', line=dict(color='#FF6B35', width=3),
                                 marker=dict(size=8, color='#FF6B35', line=dict(width=2, color='white'))))
        fig.update_layout(
            height=320, margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", y=1.1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Active Alerts</div>', unsafe_allow_html=True)
        for alert in st.session_state.alerts[:5]:
            severity = alert.severity.value
            css_class = f"alert-{severity}"
            st.markdown(
                f'<div class="{css_class}">'
                f'<strong>{alert.title}</strong><br>'
                f'<span style="font-size:0.85rem;">{alert.message}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- AI Insights ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Insights</div>', unsafe_allow_html=True)
    insights = st.session_state.insights
    cols = st.columns(min(len(insights), 4))
    impact_colors = {"high": "#dc3545", "critical": "#dc3545", "medium": "#ffc107", "low": "#28a745"}
    for i, insight in enumerate(insights[:4]):
        with cols[i]:
            border_color = impact_colors.get(insight['impact'], '#FF6B35')
            st.markdown(
                f'<div class="insight-card" style="border-left-color:{border_color};">'
                f'<div class="insight-title">{insight["title"]}</div>'
                f'<div class="insight-desc">{insight["description"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # --- Platform Architecture Diagram ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Platform Architecture</div>', unsafe_allow_html=True)
    st.markdown(render_svg(PLATFORM_ARCHITECTURE_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Bottom Row: Health, Forecast, Stats ---
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Inventory Health</div>', unsafe_allow_html=True)
        st.markdown(render_svg(health_gauge_svg(health), width="150px"), unsafe_allow_html=True)
        status_text = "Excellent" if health >= 80 else "Good" if health >= 60 else "Needs Attention" if health >= 40 else "Critical"
        status_color = "#28a745" if health >= 80 else "#ffc107" if health >= 60 else "#dc3545"
        st.markdown(f'<p style="text-align:center;font-weight:700;color:{status_color};">{status_text}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center;font-size:0.85rem;color:#636e72;">{inv_analysis["low_stock_count"]} items low | {inv_analysis["total_items"]} total</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Today\'s Forecast</div>', unsafe_allow_html=True)
        if forecasts:
            today_fc = forecasts[0]
            st.markdown(f'<div style="text-align:center;">'
                       f'<div style="font-size:3rem;font-weight:800;color:#FF6B35;">{today_fc.predicted_covers}</div>'
                       f'<div style="font-size:0.85rem;color:#636e72;">Expected Covers</div>'
                       f'<div style="font-size:1.5rem;font-weight:700;color:#2D3436;margin-top:0.5rem;">{fmt(today_fc.predicted_revenue)}</div>'
                       f'<div style="font-size:0.85rem;color:#636e72;">Expected Revenue</div>'
                       f'<div style="margin-top:0.8rem;font-size:0.9rem;">'
                       f'<span style="color:#FF6B35;font-weight:600;">{today_fc.day_of_week}</span>'
                       f'</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Quick Stats</div>', unsafe_allow_html=True)
        total_revenue_30d = sum(d['total_revenue'] for d in orders[-30:])
        total_covers_30d = sum(d['total_covers'] for d in orders[-30:])
        avg_check = sum(d['avg_check'] for d in orders[-7:]) / 7
        st.markdown(
            f'<div style="padding:0.5rem 0;">'
            f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="color:#636e72;font-size:0.9rem;">30-Day Revenue</span>'
            f'<span style="font-weight:700;color:#2D3436;">{fmt(total_revenue_30d)}</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="color:#636e72;font-size:0.9rem;">30-Day Covers</span>'
            f'<span style="font-weight:700;color:#2D3436;">{total_covers_30d:,}</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="color:#636e72;font-size:0.9rem;">Avg Check</span>'
            f'<span style="font-weight:700;color:#2D3436;">{fmt(avg_check)}</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="color:#636e72;font-size:0.9rem;">Menu Items</span>'
            f'<span style="font-weight:700;color:#2D3436;">{len(st.session_state.menu)}</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;">'
            f'<span style="color:#636e72;font-size:0.9rem;">Active Suppliers</span>'
            f'<span style="font-weight:700;color:#2D3436;">{len(st.session_state.suppliers)}</span></div>'
            f'</div>', unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
