"""Inventory Management Page - Enhanced"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from inventory.optimizer import InventoryOptimizer
from web.assets.images import render_svg, health_gauge_svg, INVENTORY_HEADER_SVG
from web.utils.currency import fmt, fmt_rate, currency_label, convert


def show():
    st.markdown('<p class="main-header">Inventory Management</p>', unsafe_allow_html=True)
    st.markdown(render_svg(INVENTORY_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">AI-optimized inventory tracking, health monitoring, and waste reduction.</p>', unsafe_allow_html=True)

    optimizer = InventoryOptimizer()
    inventory = st.session_state.inventory
    analysis = optimizer.analyze_inventory(inventory)

    # KPIs with gauge
    col1, col2, col3, col4, col5 = st.columns(5)
    kpis = [
        ("kpi-icon-blue", "📦", str(analysis['total_items']), "TOTAL ITEMS"),
        ("kpi-icon-green", "💰", fmt(analysis['total_value']), "INVENTORY VALUE"),
        ("kpi-icon-orange", "🗑️", f"{analysis['avg_wastage']}%", "AVG WASTE"),
        ("kpi-icon-red", "⚠️", str(analysis['low_stock_count']), "LOW STOCK"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f'''<div class="kpi-card">
                <div class="kpi-icon {icon_cls}">{emoji}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>''', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="kpi-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(render_svg(health_gauge_svg(analysis['health_score']), width="100px"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 Inventory List", "📉 Waste Analysis", "📊 Analytics"])

    with tab1:
        show_inventory_list(inventory)
    with tab2:
        show_waste_analysis(optimizer, inventory)
    with tab3:
        show_inventory_analytics(analysis, inventory)


def show_inventory_list(inventory):
    st.markdown('<div class="section-title">Current Inventory</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by status:", ["All", "Low Stock", "Out of Stock", "Normal", "Overstocked"])
    with col2:
        cat_filter = st.selectbox("Filter by category:", ["All"] + list(set(i.category.value for i in inventory)))

    filtered = inventory
    if status_filter == "Low Stock":
        filtered = [i for i in filtered if i.stock_status == "low"]
    elif status_filter == "Out of Stock":
        filtered = [i for i in filtered if i.stock_status == "out_of_stock"]
    elif status_filter == "Normal":
        filtered = [i for i in filtered if i.stock_status == "normal"]
    elif status_filter == "Overstocked":
        filtered = [i for i in filtered if i.stock_status == "overstocked"]

    if cat_filter != "All":
        filtered = [i for i in filtered if i.category.value == cat_filter]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    table_data = []
    for item in filtered:
        status_badge = {
            "out_of_stock": '<span class="badge badge-danger">OUT</span>',
            "low": '<span class="badge badge-warning">LOW</span>',
            "normal": '<span class="badge badge-normal">OK</span>',
            "overstocked": '<span class="badge badge-medium">OVER</span>'
        }.get(item.stock_status, "")
        table_data.append({
            "Status": {"out_of_stock": "OUT", "low": "LOW", "normal": "OK", "overstocked": "OVER"}.get(item.stock_status, "?"),
            "Name": item.name,
            "Category": item.category.value,
            "Stock": f"{item.current_stock} {item.unit}",
            "Reorder Pt": f"{item.reorder_point} {item.unit}",
            "Days Left": f"{item.days_remaining:.0f}" if item.days_remaining < 999 else "N/A",
            "Unit Cost": fmt_rate(item.unit_cost),
            "Waste %": f"{item.wastage_pct}%",
            "Value": fmt(item.current_stock * item.unit_cost)
        })
    st.dataframe(table_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_waste_analysis(optimizer, inventory):
    st.markdown('<div class="section-title">Food Waste Analysis</div>', unsafe_allow_html=True)
    waste = optimizer.calculate_waste_metrics(inventory)

    col1, col2, col3 = st.columns(3)
    waste_kpis = [
        ("kpi-icon-red", "💸", fmt(waste['total_waste_cost_monthly']), "MONTHLY WASTE COST"),
        ("kpi-icon-orange", "📊", f"{waste['avg_wastage_pct']}%", "AVG WASTAGE"),
        ("kpi-icon-green", "💰", fmt(waste['potential_savings'], compact=False) + "/mo", "POTENTIAL SAVINGS"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3], waste_kpis):
        with col:
            st.markdown(f'''<div class="kpi-card">
                <div class="kpi-icon {icon_cls}">{emoji}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Waste by category
    if waste.get('waste_by_category'):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Waste % by Category</div>', unsafe_allow_html=True)
        cats = list(waste['waste_by_category'].keys())
        vals = [waste['waste_by_category'][c] for c in cats]
        colors = ['#dc3545' if v > 8 else '#ffc107' if v > 5 else '#28a745' for v in vals]
        fig = go.Figure(go.Bar(x=cats, y=vals, marker_color=colors, marker_line=dict(width=0)))
        fig.update_layout(height=350, yaxis_title="Waste %",
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"))
        fig.add_hline(y=5, line_dash="dash", annotation_text="Target 5%", line_color="#636e72")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # High waste items
    if waste.get('high_waste_items'):
        st.markdown('<div class="section-title">High Waste Items (&gt;8%)</div>', unsafe_allow_html=True)
        for item in waste['high_waste_items']:
            st.markdown(
                f'<div class="alert-high">'
                f'<strong>{item["name"]}</strong> - {item["wastage_pct"]}% waste '
                f'({fmt(item["waste_cost"])}/week)'
                f'</div>',
                unsafe_allow_html=True
            )


def show_inventory_analytics(analysis, inventory):
    st.markdown('<div class="section-title">Inventory Analytics</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if analysis.get('by_category'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Value by Category</div>', unsafe_allow_html=True)
            cats = list(analysis['by_category'].keys())
            vals = [convert(analysis['by_category'][c]['value']) for c in cats]
            fig = go.Figure(data=[go.Pie(labels=cats, values=vals, hole=0.45,
                                         marker_colors=px.colors.qualitative.Set3)])
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        days_data = [(i.name, min(i.days_remaining, 30)) for i in inventory if i.days_remaining < 999]
        if days_data:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Days of Stock Remaining</div>', unsafe_allow_html=True)
            names, days = zip(*sorted(days_data, key=lambda x: x[1]))
            colors = ['#dc3545' if d < 3 else '#ffc107' if d < 7 else '#28a745' for d in days]
            fig = go.Figure(go.Bar(x=list(names), y=list(days), marker_color=colors,
                                   marker_line=dict(width=0)))
            fig.update_layout(height=400, yaxis_title="Days", xaxis_tickangle=-45,
                             plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                             xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"))
            fig.add_hline(y=3, line_dash="dash", line_color="#dc3545", annotation_text="Critical")
            fig.add_hline(y=7, line_dash="dash", line_color="#ffc107", annotation_text="Low")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
