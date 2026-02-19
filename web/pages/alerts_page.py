"""Alerts Page - Enhanced"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import render_svg, ALERTS_HEADER_SVG


def show():
    st.markdown(render_svg(ALERTS_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">AI-generated alerts with recommended actions and priority levels.</p>', unsafe_allow_html=True)

    alerts = st.session_state.alerts
    unread = [a for a in alerts if not a.is_read]

    # KPI cards
    critical = sum(1 for a in alerts if a.severity.value == "critical")
    high = sum(1 for a in alerts if a.severity.value == "high")

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("kpi-icon-blue", "📋", str(len(alerts)), "TOTAL ALERTS"),
        ("kpi-icon-orange", "📬", str(len(unread)), "UNREAD"),
        ("kpi-icon-red", "🚨", str(critical), "CRITICAL"),
        ("kpi-icon-purple", "⚠️", str(high), "HIGH PRIORITY"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f'''<div class="kpi-card">
                <div class="kpi-icon {icon_cls}">{emoji}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter
    severity_filter = st.selectbox("Filter by severity:", ["All", "Critical", "High", "Medium", "Low"])
    filtered = alerts if severity_filter == "All" else [a for a in alerts if a.severity.value == severity_filter.lower()]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Alerts ({len(filtered)} shown)</div>', unsafe_allow_html=True)

    for alert in filtered:
        severity = alert.severity.value
        css_class = f"alert-{severity}" if severity in ('critical', 'high', 'medium', 'low') else "alert-medium"
        badge_class = f"badge-{severity}" if severity in ('critical', 'high', 'medium', 'low') else "badge-medium"
        severity_label = severity.upper()

        action_html = ""
        if alert.recommended_action:
            action_html = (
                f'<div style="margin-top:0.6rem;padding:0.6rem;background:rgba(255,255,255,0.6);'
                f'border-radius:8px;font-size:0.85rem;">'
                f'<strong style="color:#FF6B35;">Recommended Action:</strong> {alert.recommended_action}</div>'
            )

        st.markdown(
            f'<div class="{css_class}">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            f'<div>'
            f'<span class="badge {badge_class}">{severity_label}</span> '
            f'<span style="font-size:0.8rem;color:#636e72;margin-left:0.5rem;">{alert.category.upper()}</span>'
            f'<div style="font-weight:700;font-size:1rem;margin-top:0.4rem;">{alert.title}</div>'
            f'<div style="font-size:0.9rem;color:#4a4a4a;margin-top:0.2rem;">{alert.message}</div>'
            f'</div></div>'
            f'{action_html}'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
