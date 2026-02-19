"""Suppliers Management Page - Enhanced with premium visuals"""
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import render_svg, supplier_badge_svg, SUPPLIERS_HEADER_SVG
from web.utils.currency import fmt, fmt_rate, currency_label, convert


def show():
    st.markdown('<p class="main-header">Supplier Management</p>', unsafe_allow_html=True)
    st.markdown(render_svg(SUPPLIERS_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">Monitor supplier performance, compare reliability metrics, and manage vendor relationships.</p>', unsafe_allow_html=True)

    suppliers = st.session_state.suppliers

    # --- KPI Row ---
    total_suppliers = len(suppliers)
    avg_reliability = sum(s.reliability_score for s in suppliers) / total_suppliers * 100 if total_suppliers else 0
    avg_fill_rate = sum(s.avg_fill_rate for s in suppliers) / total_suppliers * 100 if total_suppliers else 0
    avg_lead_time = sum(s.lead_time_days for s in suppliers) / total_suppliers if total_suppliers else 0

    col1, col2, col3, col4 = st.columns(4)

    def kpi_html(icon_class, icon_text, value, label):
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_text}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>'''

    with col1:
        st.markdown(kpi_html("kpi-icon-orange", "&#x1f3ed;", f"{total_suppliers}", "TOTAL SUPPLIERS"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_html("kpi-icon-green", "&#x2714;", f"{avg_reliability:.0f}%", "AVG RELIABILITY"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_html("kpi-icon-blue", "&#x1f4e6;", f"{avg_fill_rate:.0f}%", "AVG FILL RATE"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_html("kpi-icon-purple", "&#x23f1;", f"{avg_lead_time:.1f}d", "AVG LEAD TIME"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Supplier Directory", "Performance"])

    with tab1:
        show_supplier_list(suppliers)
    with tab2:
        show_performance(suppliers)


def show_supplier_list(suppliers):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Supplier Directory</div>', unsafe_allow_html=True)
    table = []
    for s in suppliers:
        table.append({
            "Name": s.name,
            "Tier": s.tier.value.title(),
            "Categories": ", ".join(c.value for c in s.categories),
            "City": s.city,
            "Lead Time": f"{s.lead_time_days}d",
            "Min Order": fmt(s.min_order_value),
            "Reliability": f"{s.reliability_score*100:.0f}%",
            "Fill Rate": f"{s.avg_fill_rate*100:.0f}%",
            "Total Orders": s.total_orders,
            "Total Value": fmt(s.total_value)
        })
    st.dataframe(table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Detail view
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Supplier Details</div>', unsafe_allow_html=True)
    selected = st.selectbox("View supplier details:", [s.name for s in suppliers])
    supplier = next((s for s in suppliers if s.name == selected), None)
    if supplier:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<div style="padding:0.5rem 0;">'
                f'<div style="font-size:1.2rem;font-weight:700;color:#2D3436;margin-bottom:0.5rem;">{supplier.name}</div>'
                f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
                f'<span style="color:#636e72;font-size:0.9rem;">Tier</span>'
                f'<span style="font-weight:600;color:#2D3436;">{supplier.tier.value.title()}</span></div>'
                f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
                f'<span style="color:#636e72;font-size:0.9rem;">Location</span>'
                f'<span style="font-weight:600;color:#2D3436;">{supplier.city}, {supplier.country}</span></div>'
                f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">'
                f'<span style="color:#636e72;font-size:0.9rem;">Categories</span>'
                f'<span style="font-weight:600;color:#2D3436;">{", ".join(c.value for c in supplier.categories)}</span></div>'
                f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;">'
                f'<span style="color:#636e72;font-size:0.9rem;">Min Order</span>'
                f'<span style="font-weight:600;color:#2D3436;">{fmt(supplier.min_order_value)}</span></div>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.metric("Reliability", f"{supplier.reliability_score*100:.0f}%")
            st.metric("Fill Rate", f"{supplier.avg_fill_rate*100:.0f}%")
            st.metric("Lead Time", f"{supplier.lead_time_days} days")
    st.markdown('</div>', unsafe_allow_html=True)


def show_performance(suppliers):
    # --- Supplier Badges ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Supplier Scorecard</div>', unsafe_allow_html=True)
    badge_cols = st.columns(min(len(suppliers), 4))
    for i, s in enumerate(suppliers):
        with badge_cols[i % len(badge_cols)]:
            score = int(s.reliability_score * 100)
            tier = s.tier.value
            st.markdown(render_svg(supplier_badge_svg(s.name, score, tier), width="100%"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Reliability & Fill Rate Chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Reliability and Fill Rate Comparison</div>', unsafe_allow_html=True)

    names = [s.name for s in suppliers]
    reliability = [s.reliability_score * 100 for s in suppliers]
    fill_rates = [s.avg_fill_rate * 100 for s in suppliers]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=reliability, name="Reliability %",
        marker_color="#FF6B35", marker_line=dict(width=0)
    ))
    fig.add_trace(go.Bar(
        x=names, y=fill_rates, name="Fill Rate %",
        marker_color="#2c3e50", marker_line=dict(width=0)
    ))
    fig.update_layout(
        height=400, barmode="group",
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(title="%", gridcolor="#f0f0f0")
    )
    fig.add_hline(y=90, line_dash="dash", annotation_text="Target 90%",
                  annotation_position="top left", line_color="#636e72")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Lead Time Chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Lead Time Comparison</div>', unsafe_allow_html=True)

    lead_times = [s.lead_time_days for s in suppliers]
    colors = ['#28a745' if lt <= 1 else '#ffc107' if lt <= 2 else '#dc3545' for lt in lead_times]

    fig2 = go.Figure(go.Bar(
        x=names, y=lead_times,
        marker_color=colors, marker_line=dict(width=0)
    ))
    fig2.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(title="Days", gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Forkast Impact Metrics ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Forkast Impact on Supplier Metrics</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#636e72;font-size:0.9rem;margin-bottom:1rem;">Comparison of pre-Forkast vs post-Forkast operational metrics:</p>', unsafe_allow_html=True)

    metrics_data = [
        {"Metric": "Order Accuracy", "Pre-Forkast": "78%", "Post-Forkast": "95%", "Change": "+17 pp"},
        {"Metric": "Stockout Frequency", "Pre-Forkast": "15%", "Post-Forkast": "5%", "Change": "-10 pp"},
        {"Metric": "Lead Time Variance", "Pre-Forkast": "+/-3 days", "Post-Forkast": "+/-0.8 days", "Change": "-2.2 days"},
        {"Metric": "Supplier Retention", "Pre-Forkast": "62%", "Post-Forkast": "84%", "Change": "+22 pp"},
        {"Metric": "Revenue Predictability", "Pre-Forkast": "+/-20%", "Post-Forkast": "+/-6%", "Change": "-14 pp"},
    ]
    st.dataframe(metrics_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
