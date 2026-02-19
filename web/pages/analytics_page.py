"""Analytics & Growth Metrics Page - Enhanced with premium visuals"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import (
    render_svg, GROWTH_PILOT_SVG, GROWTH_SCALE_SVG, GROWTH_NETWORK_SVG,
    ANALYTICS_HEADER_SVG, NETWORK_EFFECTS_SVG, DATA_FLOW_ARCHITECTURE_SVG
)
from web.utils.currency import fmt, fmt_rate, currency_label, convert


def show():
    st.markdown('<p class="main-header">Analytics & Growth</p>', unsafe_allow_html=True)
    st.markdown(render_svg(ANALYTICS_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">Track operational performance, financial health, and growth trajectory across your restaurant.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Operations", "Financial", "Growth Model"])

    with tab1:
        show_operations_analytics()
    with tab2:
        show_financial_analytics()
    with tab3:
        show_growth_model()


def show_operations_analytics():
    orders = st.session_state.historical_orders

    # --- KPI summary row ---
    last_7 = orders[-7:]
    prev_7 = orders[-14:-7]
    avg_covers_7 = sum(d['total_covers'] for d in last_7) / 7
    prev_covers_7 = sum(d['total_covers'] for d in prev_7) / 7
    covers_delta = ((avg_covers_7 - prev_covers_7) / prev_covers_7 * 100) if prev_covers_7 > 0 else 0

    avg_waste_7 = sum(d.get('food_waste_kg', 0) for d in last_7) / 7
    prev_waste_7 = sum(d.get('food_waste_kg', 0) for d in prev_7) / 7
    waste_delta = ((avg_waste_7 - prev_waste_7) / prev_waste_7 * 100) if prev_waste_7 > 0 else 0

    total_covers_90 = sum(d['total_covers'] for d in orders)

    col1, col2, col3 = st.columns(3)

    def kpi_html(icon_class, icon_emoji, value, label, delta=None, delta_up=True):
        delta_html = ""
        if delta is not None:
            cls = "kpi-delta-up" if delta_up else "kpi-delta-down"
            arrow = "+" if delta_up else ""
            delta_html = f'<div class="kpi-delta {cls}">{arrow}{delta:.1f}% vs prev week</div>'
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_emoji}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {delta_html}
        </div>'''

    with col1:
        st.markdown(kpi_html("kpi-icon-orange", "👥", f"{avg_covers_7:.0f}", "AVG DAILY COVERS (7D)",
                             covers_delta, covers_delta >= 0), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_html("kpi-icon-red", "🗑️", f"{avg_waste_7:.1f} kg", "AVG DAILY WASTE (7D)",
                             waste_delta, waste_delta <= 0), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_html("kpi-icon-blue", "📊", f"{total_covers_90:,}", "TOTAL COVERS (90D)"),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Daily covers trend ---
    dates = [d['date'] for d in orders]
    covers = [d['total_covers'] for d in orders]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Daily Covers (90 Days)</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=covers, mode='lines', name='Daily Covers',
        line=dict(color='#FF6B35', width=1.5), opacity=0.6
    ))
    # 7-day moving average
    ma7 = [sum(covers[max(0, i - 6):i + 1]) / min(7, i + 1) for i in range(len(covers))]
    fig.add_trace(go.Scatter(
        x=dates, y=ma7, mode='lines', name='7-Day Avg',
        line=dict(color='#2c3e50', width=3)
    ))
    fig.update_layout(
        height=400, margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0", title="Covers")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Day-of-week analysis and waste trend side by side ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Average Covers by Day of Week</div>', unsafe_allow_html=True)

        dow_data = defaultdict(list)
        for d in orders:
            dow_data[d['day_of_week']].append(d['total_covers'])

        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        avg_by_dow = {d: sum(dow_data[d]) / len(dow_data[d]) for d in dow_order if d in dow_data}

        fig2 = go.Figure(go.Bar(
            x=list(avg_by_dow.keys()), y=list(avg_by_dow.values()),
            marker_color=['#FF6B35' if d in ['Thursday', 'Friday', 'Saturday'] else '#6c757d' for d in avg_by_dow.keys()],
            marker_line=dict(width=0)
        ))
        fig2.update_layout(
            height=350, margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0", title="Avg Covers")
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Daily Food Waste (kg)</div>', unsafe_allow_html=True)

        waste = [d.get('food_waste_kg', 0) for d in orders]
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=dates, y=waste, mode='lines', name='Food Waste (kg)',
            line=dict(color='#dc3545', width=1.5), opacity=0.6
        ))
        waste_ma = [sum(waste[max(0, i - 6):i + 1]) / min(7, i + 1) for i in range(len(waste))]
        fig3.add_trace(go.Scatter(
            x=dates, y=waste_ma, mode='lines', name='7-Day Avg',
            line=dict(color='#2c3e50', width=3)
        ))
        fig3.update_layout(
            height=350, margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", y=1.1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0", title="Waste (kg)")
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def show_financial_analytics():
    orders = st.session_state.historical_orders

    dates = [d['date'] for d in orders]
    revenues = [d['total_revenue'] for d in orders]
    food_costs = [d.get('food_cost_pct', 30) for d in orders]
    labor_costs = [d.get('labor_cost_pct', 25) for d in orders]

    # --- Financial KPIs ---
    total_30d = sum(revenues[-30:])
    avg_check = sum(d['avg_check'] for d in orders[-30:]) / 30
    avg_food = sum(food_costs[-30:]) / 30
    avg_labor = sum(labor_costs[-30:]) / 30

    prev_30d = sum(revenues[-60:-30]) if len(revenues) >= 60 else sum(revenues[:30])
    rev_delta = ((total_30d - prev_30d) / prev_30d * 100) if prev_30d > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    def kpi_html(icon_class, icon_emoji, value, label, delta=None, delta_up=True):
        delta_html = ""
        if delta is not None:
            cls = "kpi-delta-up" if delta_up else "kpi-delta-down"
            arrow = "+" if delta_up else ""
            delta_html = f'<div class="kpi-delta {cls}">{arrow}{delta:.1f}% vs prev period</div>'
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_emoji}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {delta_html}
        </div>'''

    with col1:
        st.markdown(kpi_html("kpi-icon-green", "💰", fmt(total_30d), "30-DAY REVENUE",
                             rev_delta, rev_delta >= 0), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_html("kpi-icon-orange", "🧾", fmt(avg_check), "AVG CHECK"),
                    unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_html("kpi-icon-red", "🍖", f"{avg_food:.1f}%", "FOOD COST %"),
                    unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_html("kpi-icon-blue", "👥", f"{avg_labor:.1f}%", "LABOR COST %"),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Revenue trend ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Daily Revenue ({currency_label()}) - 90 Days</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dates, y=[convert(r) for r in revenues], name='Revenue',
        marker_color='#FF6B35', opacity=0.6,
        marker_line=dict(width=0)
    ))
    rev_ma = [sum(revenues[max(0, i - 6):i + 1]) / min(7, i + 1) for i in range(len(revenues))]
    fig.add_trace(go.Scatter(
        x=dates, y=[convert(v) for v in rev_ma], mode='lines', name='7-Day Avg',
        line=dict(color='#2c3e50', width=3)
    ))
    fig.update_layout(
        height=400, margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0", title=f"Revenue ({currency_label()})")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Cost structure and cost trend side by side ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cost Structure (Last 30 Days)</div>', unsafe_allow_html=True)

        avg_other = 100 - avg_food - avg_labor - 12  # 12% profit assumption

        fig2 = go.Figure(data=[go.Pie(
            labels=['Food Cost', 'Labor Cost', 'Other Costs', 'Profit'],
            values=[avg_food, avg_labor, max(0, avg_other), 12],
            marker_colors=['#FF6B35', '#2c3e50', '#6c757d', '#28a745'],
            hole=0.5,
            textinfo='label+percent', textfont=dict(size=12)
        )])
        fig2.update_layout(
            height=380, margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cost % Trends (90 Days)</div>', unsafe_allow_html=True)

        food_ma = [sum(food_costs[max(0, i - 6):i + 1]) / min(7, i + 1) for i in range(len(food_costs))]
        labor_ma = [sum(labor_costs[max(0, i - 6):i + 1]) / min(7, i + 1) for i in range(len(labor_costs))]

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=dates, y=food_ma, mode='lines', name='Food Cost %',
            line=dict(color='#FF6B35', width=2.5)
        ))
        fig3.add_trace(go.Scatter(
            x=dates, y=labor_ma, mode='lines', name='Labor Cost %',
            line=dict(color='#2c3e50', width=2.5)
        ))
        fig3.update_layout(
            height=380, margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", y=1.1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0", title="Cost %")
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def show_growth_model():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Forkast Growth Forecast Model</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-desc">Bottom-up, cohort-based, city-by-city growth model.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Growth phase SVGs ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Growth Phases</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_svg(GROWTH_PILOT_SVG, width="140px"), unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:center;padding:0.5rem 0;">'
            f'<div style="font-weight:700;color:#FF6B35;font-size:1rem;">Pilot (Q1-Q2)</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">5-20 kitchens</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">{currency_label()} 15K-50K/mo</div>'
            f'<div style="font-size:0.8rem;color:#2D3436;margin-top:0.3rem;font-weight:500;">Prove value, gather data</div>'
            f'</div>', unsafe_allow_html=True
        )
    with col2:
        st.markdown(render_svg(GROWTH_SCALE_SVG, width="140px"), unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:center;padding:0.5rem 0;">'
            f'<div style="font-weight:700;color:#28a745;font-size:1rem;">Scale (Q3-Q4)</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">50-150 kitchens</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">{currency_label()} 200K-600K/mo</div>'
            f'<div style="font-size:0.8rem;color:#2D3436;margin-top:0.3rem;font-weight:500;">City density, supplier onboarding</div>'
            f'</div>', unsafe_allow_html=True
        )
    with col3:
        st.markdown(render_svg(GROWTH_NETWORK_SVG, width="140px"), unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:center;padding:0.5rem 0;">'
            f'<div style="font-weight:700;color:#1565C0;font-size:1rem;">Network Effect (Y2)</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">300+ kitchens</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">{currency_label()} 1.5M+/mo</div>'
            f'<div style="font-size:0.8rem;color:#2D3436;margin-top:0.3rem;font-weight:500;">Cross-city expansion, data moat</div>'
            f'</div>', unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # --- Scenario analysis ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Adoption Scenarios (24 Months)</div>', unsafe_allow_html=True)

    months = list(range(1, 25))

    conservative = [min(5 + i * 2, 80) for i in months]
    base = [min(5 + i * 4, 200) for i in months]
    upside = [min(5 + i * 7, 400) for i in months]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=upside, fill=None, mode='lines',
        name='Upside', line=dict(color='#28a745', dash='dash', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=months, y=base, mode='lines',
        name='Base Case', line=dict(color='#FF6B35', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=months, y=conservative, mode='lines',
        name='Conservative', line=dict(color='#6c757d', dash='dash', width=2)
    ))
    fig.update_layout(
        height=400, margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0", title="Month"),
        yaxis=dict(gridcolor="#f0f0f0", title="Active Kitchens")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- CLV comparison and Network Effects side by side ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Customer Lifetime Value (CLV)</div>', unsafe_allow_html=True)

        # CLV bar comparison
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=['Non-AI User', 'AI-Enabled (Forkast)'],
            y=[convert(1333), convert(4200)],
            marker_color=['#6c757d', '#FF6B35'],
            marker_line=dict(width=0),
            text=[fmt(1333), fmt(4200)],
            textposition='outside',
            textfont=dict(size=14, color='#2D3436')
        ))
        fig2.update_layout(
            height=300, margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0", title=f"CLV ({currency_label()})")
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            '<div style="padding:0.8rem;background:linear-gradient(135deg,#f0fff4 0%,#c6f6d5 100%);'
            'border-radius:10px;border-left:4px solid #28a745;">'
            '<strong style="color:#28a745;">Forkast triples CLV</strong>'
            '<span style="color:#636e72;font-size:0.9rem;"> by increasing ARPA through premium features '
            'and reducing churn via operational stickiness.</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Detail table
        st.markdown(
            f'<div style="font-size:0.85rem;">'
            f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f0f0f0;font-weight:700;color:#2D3436;">'
            f'<span style="flex:2;">Metric</span><span style="flex:1;text-align:center;">Non-AI</span><span style="flex:1;text-align:center;">Forkast</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="flex:2;color:#636e72;">ARPA ({currency_label()})</span><span style="flex:1;text-align:center;">{fmt(80, show_symbol=False)}</span><span style="flex:1;text-align:center;color:#FF6B35;font-weight:600;">{fmt(140, show_symbol=False)}</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="flex:2;color:#636e72;">Gross Margin</span><span style="flex:1;text-align:center;">75%</span><span style="flex:1;text-align:center;">75%</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<span style="flex:2;color:#636e72;">Monthly Churn</span><span style="flex:1;text-align:center;">4.5%</span><span style="flex:1;text-align:center;color:#28a745;font-weight:600;">2.5%</span></div>'
            f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;">'
            f'<span style="flex:2;color:#636e72;">CLV ({currency_label()})</span><span style="flex:1;text-align:center;">{fmt(1333, show_symbol=False)}</span><span style="flex:1;text-align:center;color:#FF6B35;font-weight:700;">{fmt(4200, show_symbol=False)}</span></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Network Effects</div>', unsafe_allow_html=True)

        # Network Effects SVG Graphic
        st.markdown(render_svg(NETWORK_EFFECTS_SVG, width="100%"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Revenue per kitchen projection
        st.markdown('<div class="section-title">Revenue per Kitchen Projection</div>', unsafe_allow_html=True)

        months_proj = list(range(1, 25))
        rev_per_kitchen = [convert(80 + (i * 2.5)) for i in months_proj]  # ARPA grows with network

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=months_proj, y=rev_per_kitchen, mode='lines+markers',
            name=f'ARPA ({currency_label()})', line=dict(color='#FF6B35', width=3),
            marker=dict(size=6, color='#FF6B35', line=dict(width=1.5, color='white'))
        ))
        fig3.add_trace(go.Scatter(
            x=months_proj, y=[convert(80)] * len(months_proj), mode='lines',
            name='Non-AI Baseline', line=dict(color='#6c757d', dash='dot', width=2)
        ))
        fig3.update_layout(
            height=280, margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", y=1.15),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0", title="Month"),
            yaxis=dict(gridcolor="#f0f0f0", title=f"ARPA ({currency_label()})")
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Data Flow Architecture Diagram (full width) ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Platform Data Flow</div>', unsafe_allow_html=True)
    st.markdown(render_svg(DATA_FLOW_ARCHITECTURE_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
