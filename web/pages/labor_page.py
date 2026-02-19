"""Labor Scheduling Page - Enhanced with premium styling"""
import streamlit as st
import plotly.graph_objects as go
from collections import defaultdict
from datetime import date, timedelta

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.utils.currency import fmt, fmt_rate, currency_label, convert
from web.assets.images import render_svg, LABOR_HEADER_SVG


def show():
    st.markdown('<p class="main-header">Labor Scheduling</p>', unsafe_allow_html=True)
    st.markdown(render_svg(LABOR_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">AI-optimized staff scheduling based on demand forecasts and labor cost analytics.</p>',
        unsafe_allow_html=True,
    )

    schedule = st.session_state.staff_schedule
    forecasts = st.session_state.forecasts

    # --- KPI Summary Cards ---
    total_hours = sum(s.hours for s in schedule)
    total_cost = sum(s.hours * s.hourly_rate for s in schedule)
    unique_staff = len(set(s.staff_name for s in schedule))
    peak_days = len(set(s.shift_date for s in schedule if s.is_peak))
    avg_cost_per_hour = total_cost / total_hours if total_hours > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    kpis = [
        ("kpi-icon-orange", "&#128337;", f"{total_hours:.0f}", "TOTAL HOURS"),
        ("kpi-icon-green", "&#128176;", fmt(total_cost), "LABOR COST"),
        ("kpi-icon-blue", "&#9881;", fmt_rate(avg_cost_per_hour), "AVG COST / HR"),
        ("kpi-icon-purple", "&#128100;", str(unique_staff), "ACTIVE STAFF"),
        ("kpi-icon-red", "&#9650;", str(peak_days), "PEAK DAYS"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3, col4, col5], kpis):
        with col:
            st.markdown(
                f'''<div class="kpi-card">
                    <div class="kpi-icon {icon_cls}">{emoji}</div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-label">{lbl}</div>
                </div>''',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Weekly Schedule", "Labor Analytics", "Optimization"])

    with tab1:
        show_weekly_schedule(schedule)
    with tab2:
        show_labor_analytics(schedule)
    with tab3:
        show_optimization(schedule, forecasts)


def show_weekly_schedule(schedule):
    st.markdown('<div class="section-title">Weekly Staff Schedule</div>', unsafe_allow_html=True)

    # Group by date
    by_date = defaultdict(list)
    for s in schedule:
        by_date[s.shift_date].append(s)

    for shift_date in sorted(by_date.keys()):
        day_schedule = by_date[shift_date]
        day_name = shift_date.strftime("%A")
        is_peak = any(s.is_peak for s in day_schedule)
        peak_tag = "  [PEAK]" if is_peak else ""

        with st.expander(f"**{day_name} {shift_date}** - {len(day_schedule)} staff{peak_tag}"):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            table = []
            for s in sorted(day_schedule, key=lambda x: x.shift_start):
                table.append(
                    {
                        "Staff": s.staff_name,
                        "Role": s.role.replace("_", " ").title(),
                        "Shift": f"{s.shift_start} - {s.shift_end}",
                        "Hours": s.hours,
                        f"Rate ({currency_label()}/hr)": round(convert(s.hourly_rate), 2),
                        f"Cost ({currency_label()})": round(convert(s.hours * s.hourly_rate), 0),
                    }
                )
            st.dataframe(table, use_container_width=True)

            total_hours = sum(s.hours for s in day_schedule)
            total_cost = sum(s.hours * s.hourly_rate for s in day_schedule)
            st.markdown(
                f'<div style="text-align:right;padding:0.5rem 0;font-weight:600;color:#2D3436;">'
                f'Total: {total_hours:.0f} hours &nbsp;|&nbsp; {fmt(total_cost)}'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # Staffing heatmap overview
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Daily Staffing Overview</div>', unsafe_allow_html=True)

    sorted_dates = sorted(by_date.keys())
    day_labels = [d.strftime("%a %m/%d") for d in sorted_dates]
    staff_counts = [len(by_date[d]) for d in sorted_dates]
    day_hours = [sum(s.hours for s in by_date[d]) for d in sorted_dates]
    is_peak_list = [any(s.is_peak for s in by_date[d]) for d in sorted_dates]
    bar_colors = ["#FF6B35" if p else "#636e72" for p in is_peak_list]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=day_labels,
            y=staff_counts,
            name="Staff Count",
            marker_color=bar_colors,
            marker_line=dict(width=0),
            text=staff_counts,
            textposition="outside",
        )
    )
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis_title="Staff Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_labor_analytics(schedule):
    st.markdown('<div class="section-title">Labor Analytics</div>', unsafe_allow_html=True)

    # Aggregate data
    by_date = defaultdict(float)
    by_date_cost = defaultdict(float)
    by_role = defaultdict(float)
    by_role_cost = defaultdict(float)
    by_staff = defaultdict(float)
    by_staff_cost = defaultdict(float)

    for s in schedule:
        key = s.shift_date.strftime("%a %m/%d")
        by_date[key] += s.hours
        by_date_cost[key] += s.hours * s.hourly_rate
        role = s.role.replace("_", " ").title()
        by_role[role] += s.hours
        by_role_cost[role] += s.hours * s.hourly_rate
        by_staff[s.staff_name] += s.hours
        by_staff_cost[s.staff_name] += s.hours * s.hourly_rate

    days = list(by_date.keys())
    hours = [by_date[d] for d in days]
    costs = [convert(by_date_cost[d]) for d in days]

    # --- Hours and Cost by Day (side by side) ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Staff Hours by Day</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=days,
                y=hours,
                name="Hours",
                marker_color="#FF6B35",
                marker_line=dict(width=0),
            )
        )
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=10, b=20),
            yaxis_title="Total Hours",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">Labor Cost by Day ({currency_label()})</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(
            go.Bar(
                x=days,
                y=costs,
                name="Cost",
                marker_color="#2c3e50",
                marker_line=dict(width=0),
            )
        )
        fig2.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=10, b=20),
            yaxis_title=f"Cost ({currency_label()})",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0"),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Role breakdown (side by side) ---
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Hours by Role</div>', unsafe_allow_html=True)
        roles = list(by_role.keys())
        role_hours = [by_role[r] for r in roles]
        fig3 = go.Figure(
            data=[
                go.Pie(
                    labels=roles,
                    values=role_hours,
                    hole=0.45,
                    marker_colors=["#FF6B35", "#1a1a2e", "#636e72", "#17a2b8", "#6f42c1", "#28a745"],
                    textinfo="label+percent",
                    textfont=dict(size=12),
                )
            ]
        )
        fig3.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">Cost by Role ({currency_label()})</div>', unsafe_allow_html=True)
        role_costs = [convert(by_role_cost[r]) for r in roles]
        colors = ["#FF6B35", "#1a1a2e", "#636e72", "#17a2b8", "#6f42c1", "#28a745"]
        fig4 = go.Figure(
            go.Bar(
                x=roles,
                y=role_costs,
                marker_color=colors[: len(roles)],
                marker_line=dict(width=0),
                text=[fmt(c) for c in role_costs],
                textposition="outside",
            )
        )
        fig4.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=10, b=20),
            yaxis_title=f"Cost ({currency_label()})",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#f0f0f0"),
            yaxis=dict(gridcolor="#f0f0f0"),
            showlegend=False,
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Staff-level breakdown ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Hours by Staff Member</div>', unsafe_allow_html=True)

    sorted_staff = sorted(by_staff.items(), key=lambda x: x[1], reverse=True)
    staff_names = [s[0] for s in sorted_staff]
    staff_hours = [s[1] for s in sorted_staff]
    staff_costs_list = [convert(by_staff_cost[n]) for n in staff_names]

    fig5 = go.Figure()
    fig5.add_trace(
        go.Bar(
            x=staff_names,
            y=staff_hours,
            name="Hours",
            marker_color="#FF6B35",
            marker_line=dict(width=0),
        )
    )
    fig5.add_trace(
        go.Scatter(
            x=staff_names,
            y=[c / 10 for c in staff_costs_list],
            name=f"Cost ({currency_label()}/10)",
            mode="lines+markers",
            line=dict(color="#2c3e50", width=2.5),
            marker=dict(size=7, color="#2c3e50", line=dict(width=1.5, color="white")),
            yaxis="y",
        )
    )
    fig5.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis_title="Hours",
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0", tickangle=-45),
        yaxis=dict(gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Weekly Summary KPIs ---
    st.markdown("<br>", unsafe_allow_html=True)
    total_hours = sum(s.hours for s in schedule)
    total_cost = sum(s.hours * s.hourly_rate for s in schedule)
    peak_hours = sum(s.hours for s in schedule if s.is_peak)
    non_peak_hours = total_hours - peak_hours

    col1, col2, col3, col4 = st.columns(4)
    summary_kpis = [
        ("kpi-icon-orange", "&#128337;", f"{total_hours:.0f} hrs", "WEEKLY HOURS"),
        ("kpi-icon-green", "&#128176;", fmt(total_cost), "WEEKLY COST"),
        ("kpi-icon-red", "&#9650;", f"{peak_hours:.0f} hrs", "PEAK HOURS"),
        ("kpi-icon-blue", "&#9660;", f"{non_peak_hours:.0f} hrs", "NON-PEAK HOURS"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3, col4], summary_kpis):
        with col:
            st.markdown(
                f'''<div class="kpi-card">
                    <div class="kpi-icon {icon_cls}">{emoji}</div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-label">{lbl}</div>
                </div>''',
                unsafe_allow_html=True,
            )


def show_optimization(schedule, forecasts):
    st.markdown('<div class="section-title">AI Labor Optimization</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Recommendations based on demand forecast alignment with current staffing levels.</p>',
        unsafe_allow_html=True,
    )

    by_date = defaultdict(lambda: {"hours": 0, "cost": 0, "staff": 0})
    for s in schedule:
        day = s.shift_date.strftime("%A")
        by_date[day]["hours"] += s.hours
        by_date[day]["cost"] += s.hours * s.hourly_rate
        by_date[day]["staff"] += 1

    # --- Forecast vs Staffing Chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Forecast vs Staffing Alignment</div>', unsafe_allow_html=True)

    fc_days = []
    fc_covers = []
    actual_staff = []
    ideal_staff_list = []
    statuses = []

    for f in forecasts[:7]:
        day = f.day_of_week
        sched = by_date.get(day, {"hours": 0, "cost": 0, "staff": 0})
        ideal_staff = max(4, f.predicted_covers // 12)
        status = (
            "optimal"
            if abs(sched["staff"] - ideal_staff) <= 1
            else "overstaffed"
            if sched["staff"] > ideal_staff
            else "understaffed"
        )

        fc_days.append(f"{day[:3]} {f.forecast_date}")
        fc_covers.append(f.predicted_covers)
        actual_staff.append(sched["staff"])
        ideal_staff_list.append(ideal_staff)
        statuses.append(status)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=fc_days,
            y=actual_staff,
            name="Actual Staff",
            marker_color=[
                "#dc3545" if s == "understaffed" else "#ffc107" if s == "overstaffed" else "#28a745"
                for s in statuses
            ],
            marker_line=dict(width=0),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=fc_days,
            y=ideal_staff_list,
            name="Recommended Staff",
            mode="lines+markers",
            line=dict(color="#FF6B35", width=2.5, dash="dash"),
            marker=dict(size=8, color="#FF6B35", line=dict(width=2, color="white")),
        )
    )
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis_title="Staff Count",
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Day-by-Day Recommendations ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Day-by-Day Recommendations</div>', unsafe_allow_html=True)

    optimal_count = 0
    overstaffed_count = 0
    understaffed_count = 0

    for f in forecasts[:7]:
        day = f.day_of_week
        sched = by_date.get(day, {"hours": 0, "cost": 0, "staff": 0})
        ideal_staff = max(4, f.predicted_covers // 12)

        status = (
            "optimal"
            if abs(sched["staff"] - ideal_staff) <= 1
            else "overstaffed"
            if sched["staff"] > ideal_staff
            else "understaffed"
        )

        if status == "understaffed":
            understaffed_count += 1
            diff = ideal_staff - sched["staff"]
            st.markdown(
                f'<div class="alert-critical">'
                f'<strong>{day} ({f.forecast_date})</strong> &mdash; '
                f'{sched["staff"]} staff scheduled for {f.predicted_covers} predicted covers. '
                f'Recommended: {ideal_staff}. Add {diff} more staff members.'
                f'</div>',
                unsafe_allow_html=True,
            )
        elif status == "overstaffed":
            overstaffed_count += 1
            diff = sched["staff"] - ideal_staff
            st.markdown(
                f'<div class="alert-high">'
                f'<strong>{day} ({f.forecast_date})</strong> &mdash; '
                f'{sched["staff"]} staff scheduled for {f.predicted_covers} predicted covers. '
                f'Recommended: {ideal_staff}. Consider reducing by {diff}.'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            optimal_count += 1
            st.markdown(
                f'<div class="alert-low">'
                f'<strong>{day} ({f.forecast_date})</strong> &mdash; '
                f'{sched["staff"]} staff for {f.predicted_covers} predicted covers. Staffing is optimal.'
                f'</div>',
                unsafe_allow_html=True,
            )

    # --- Optimization Score ---
    st.markdown("<br>", unsafe_allow_html=True)
    total_days = optimal_count + overstaffed_count + understaffed_count
    opt_score = round((optimal_count / total_days) * 100) if total_days > 0 else 0

    col1, col2, col3 = st.columns(3)
    score_kpis = [
        ("kpi-icon-green", "&#10004;", str(optimal_count), "OPTIMAL DAYS"),
        ("kpi-icon-orange", "&#9650;", str(overstaffed_count), "OVERSTAFFED DAYS"),
        ("kpi-icon-red", "&#9660;", str(understaffed_count), "UNDERSTAFFED DAYS"),
    ]
    for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3], score_kpis):
        with col:
            st.markdown(
                f'''<div class="kpi-card">
                    <div class="kpi-icon {icon_cls}">{emoji}</div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-label">{lbl}</div>
                </div>''',
                unsafe_allow_html=True,
            )

    # --- Cost Optimization Suggestions ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Cost Optimization Suggestions</div>', unsafe_allow_html=True)

    suggestions = [
        (
            "alert-high",
            "Peak Days (Thu-Sat)",
            "Maximize full-time staff utilization. Use part-time staff for overflow only.",
        ),
        (
            "alert-low",
            "Slow Days (Mon-Wed)",
            "Reduce shift lengths where possible. Cross-train staff for multi-role flexibility.",
        ),
        (
            "alert-medium",
            "Split Shifts",
            "Consider 11:00-15:00 and 18:00-23:00 shifts on slow days to cover peaks without idle time.",
        ),
        (
            "alert-low",
            "Forecast-Based Scheduling",
            "Use the 7-day demand forecast to plan staff schedules weekly and reduce overstaffing costs.",
        ),
    ]
    for css_class, title, desc in suggestions:
        st.markdown(
            f'<div class="{css_class}">'
            f'<strong>{title}:</strong> {desc}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
