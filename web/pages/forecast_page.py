"""Demand Forecast Page - Enhanced"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import FORECAST_HEADER_SVG, render_svg
from web.utils.currency import fmt, fmt_rate, currency_label, convert


def show():
    # Dark header banner
    st.markdown(render_svg(FORECAST_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">AI-powered demand predictions with actionable insights and confidence intervals.</p>', unsafe_allow_html=True)

    engine = st.session_state.forecast_engine
    tab1, tab2, tab3 = st.tabs(["📊 Forecast", "🍽️ Item Forecast", "🧠 Model Info"])

    with tab1:
        show_demand_forecast(engine)
    with tab2:
        show_item_forecast(engine)
    with tab3:
        show_model_info(engine)


def show_demand_forecast(engine):
    days = st.slider("Forecast horizon (days):", 7, 30, 14)
    forecasts = engine.forecast(days_ahead=days)
    st.session_state.forecasts = forecasts

    # Summary KPIs in styled cards
    total_covers = sum(f.predicted_covers for f in forecasts)
    total_revenue = sum(f.predicted_revenue for f in forecasts)
    avg_daily = total_covers / days
    peak_day = max(forecasts, key=lambda f: f.predicted_covers)

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("kpi-icon-orange", "📊", f"{total_covers:,}", "TOTAL PREDICTED COVERS"),
        ("kpi-icon-green", "💰", fmt(total_revenue), "TOTAL PREDICTED REVENUE"),
        ("kpi-icon-blue", "📈", f"{avg_daily:.0f}", "AVG DAILY COVERS"),
        ("kpi-icon-purple", "🔥", f"{peak_day.day_of_week[:3]} ({peak_day.predicted_covers})", "PEAK DAY"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f'''<div class="kpi-card">
                <div class="kpi-icon {icon_cls}">{emoji}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Covers forecast chart
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Demand Forecast with Confidence Bands</div>', unsafe_allow_html=True)
    dates = [f.forecast_date.isoformat() for f in forecasts]
    covers = [f.predicted_covers for f in forecasts]
    lower = [f.confidence_lower for f in forecasts]
    upper = [f.confidence_upper for f in forecasts]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=upper, fill=None, mode='lines', line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=dates, y=lower, fill='tonexty', mode='lines', line=dict(width=0),
                             fillcolor='rgba(255,107,53,0.12)', name='95% Confidence'))
    fig.add_trace(go.Scatter(x=dates, y=covers, mode='lines+markers', name='Predicted Covers',
                             line=dict(color='#FF6B35', width=3),
                             marker=dict(size=8, color='#FF6B35', line=dict(width=2, color='white'))))
    fig.update_layout(height=400, xaxis_title="Date", yaxis_title="Covers",
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"),
                      legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Revenue forecast
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Revenue Forecast ({currency_label()})</div>', unsafe_allow_html=True)
    revenues = [convert(f.predicted_revenue) for f in forecasts]
    colors = ['#FF6B35' if f.day_of_week in ['Thursday', 'Friday', 'Saturday'] else '#b2bec3' for f in forecasts]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=dates, y=revenues, marker_color=colors, name="Revenue",
                          marker_line=dict(width=0)))
    fig2.update_layout(height=350, xaxis_title="Date", yaxis_title=f"Revenue ({currency_label()})",
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Orange bars = peak days (Thu-Sat)")
    st.markdown('</div>', unsafe_allow_html=True)

    # Channel breakdown
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Channel Breakdown</div>', unsafe_allow_html=True)
    fc_table = []
    for f in forecasts:
        fc_table.append({
            "Date": f.forecast_date.isoformat(),
            "Day": f.day_of_week[:3],
            "Covers": f.predicted_covers,
            f"Revenue ({currency_label()})": fmt(f.predicted_revenue, show_symbol=False),
            "Dine-in": f.channel_breakdown.get('dine_in', 0),
            "Delivery": f.channel_breakdown.get('delivery', 0),
            "Takeaway": f.channel_breakdown.get('takeaway', 0)
        })
    st.dataframe(fc_table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_item_forecast(engine):
    st.markdown('<div class="section-title">Item-Level Demand Forecast</div>', unsafe_allow_html=True)
    days = st.slider("Item forecast days:", 3, 14, 7, key="item_days")
    item_forecasts = engine.forecast_items(days_ahead=days)

    if not item_forecasts:
        st.info("No item-level data available.")
        return

    selected = st.selectbox("Select menu item:", sorted(item_forecasts.keys()))
    if selected and selected in item_forecasts:
        data = item_forecasts[selected]
        dates = [d['date'] for d in data]
        qtys = [d['predicted_quantity'] for d in data]

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dates, y=qtys, marker_color='#FF6B35', name=selected,
                             marker_line=dict(width=0)))
        fig.update_layout(title=f"Predicted Daily Orders: {selected}", height=350,
                         xaxis_title="Date", yaxis_title="Quantity",
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"))
        st.plotly_chart(fig, use_container_width=True)

        total = sum(qtys)
        st.markdown(f'''<div class="kpi-card" style="max-width:250px;">
            <div class="kpi-icon kpi-icon-orange">🍽️</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-label">TOTAL {selected.upper()} ({days}D)</div>
        </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # All items summary
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">All Items Forecast Summary</div>', unsafe_allow_html=True)
    summary = []
    for item_name, data in sorted(item_forecasts.items()):
        total_qty = sum(d['predicted_quantity'] for d in data)
        avg_qty = total_qty / days if days > 0 else 0
        summary.append({"Item": item_name, f"Total ({days}d)": total_qty, "Avg/Day": round(avg_qty, 1)})
    summary.sort(key=lambda x: x[f"Total ({days}d)"], reverse=True)
    st.dataframe(summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_model_info(engine):
    st.markdown('<div class="section-title">Model Information</div>', unsafe_allow_html=True)
    info = engine.get_model_summary()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Training Summary</div>', unsafe_allow_html=True)
        rows = [
            ("Training Samples", f"{info['training_samples']} days"),
            ("Base Daily Covers", str(info['base_daily_covers'])),
            ("Base Daily Revenue", fmt(info['base_daily_revenue'])),
            ("Average Check", fmt(info['avg_check'])),
            ("Trend Direction", info['trend_direction']),
            ("Items Tracked", str(info['items_tracked'])),
        ]
        for label, val in rows:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f0f0f0;">'
                f'<span style="color:#636e72;">{label}</span>'
                f'<span style="font-weight:700;color:#2D3436;">{val}</span></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Accuracy Metrics</div>', unsafe_allow_html=True)
        acc = info.get('accuracy', {})
        if acc:
            accuracy_val = acc.get('accuracy', 0)
            color = "#28a745" if accuracy_val >= 85 else "#ffc107" if accuracy_val >= 70 else "#dc3545"
            st.markdown(f'''<div style="text-align:center;padding:1rem 0;">
                <div style="font-size:3.5rem;font-weight:800;color:{color};">{accuracy_val}%</div>
                <div style="font-size:0.85rem;color:#636e72;">Forecast Accuracy</div>
                <div style="margin-top:1rem;">
                <span style="color:#636e72;font-size:0.85rem;">MAPE: </span>
                <span style="font-weight:700;">{acc.get("mape", 0)}%</span>
                <span style="color:#636e72;font-size:0.85rem;margin-left:1rem;">Holdout: </span>
                <span style="font-weight:700;">{acc.get("holdout_size", 0)} days</span>
                </div></div>''', unsafe_allow_html=True)
        else:
            st.info("Accuracy metrics not yet available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Day-of-week patterns
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Day-of-Week Patterns</div>', unsafe_allow_html=True)
    patterns = info.get('day_patterns', {})
    if patterns:
        days = list(patterns.keys())
        values = [patterns[d] * 100 for d in days]
        colors = ['#FF6B35' if v > 105 else '#28a745' if v > 95 else '#b2bec3' for v in values]
        fig = go.Figure(go.Bar(x=days, y=values, marker_color=colors,
                               marker_line=dict(width=0)))
        fig.update_layout(height=300, yaxis_title="Index (100=avg)",
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0"))
        fig.add_hline(y=100, line_dash="dash", line_color="#636e72")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Explainability
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">How Forkast Forecasts Work</div>', unsafe_allow_html=True)
    steps = [
        ("1", "Historical Pattern Analysis", "Learns from 90+ days of POS data"),
        ("2", "Day-of-Week Seasonality", "Captures weekly patterns (Thu-Sat peaks in MENA)"),
        ("3", "Monthly Seasonality", "Adjusts for Ramadan, holidays, summer dips"),
        ("4", "Trend Detection", "Identifies growth or decline patterns"),
        ("5", "Confidence Intervals", "Shows uncertainty ranges for decisions"),
        ("6", "Human-in-the-Loop", "All forecasts are recommendations, not automation"),
    ]
    for num, title, desc in steps:
        st.markdown(
            f'<div style="display:flex;gap:1rem;align-items:center;padding:0.6rem 0;border-bottom:1px solid #f0f0f0;">'
            f'<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#FF6B35,#F7931E);'
            f'display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:0.9rem;flex-shrink:0;">{num}</div>'
            f'<div><div style="font-weight:700;color:#2D3436;">{title}</div>'
            f'<div style="font-size:0.85rem;color:#636e72;">{desc}</div></div></div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
