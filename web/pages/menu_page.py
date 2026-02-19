"""Menu Optimization Page - Enhanced with premium visuals"""
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.utils.currency import fmt, fmt_rate, currency_label, convert
from web.assets.images import render_svg, MENU_HEADER_SVG


def show():
    st.markdown('<p class="main-header">Menu Optimization</p>', unsafe_allow_html=True)
    st.markdown(render_svg(MENU_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Optimize your menu based on demand, profitability, and food cost analysis. '
        'Identify stars, cut underperformers, and maximize contribution margins.</p>',
        unsafe_allow_html=True,
    )

    menu = st.session_state.menu

    # --- KPI Cards ---
    total_items = len(menu)
    avg_margin = sum(m.price - m.cost for m in menu) / total_items if total_items else 0
    avg_food_cost = sum(m.food_cost_pct for m in menu) / total_items if total_items else 0

    avg_pop = sum(m.popularity_score for m in menu) / total_items if total_items else 0
    avg_mar = avg_margin
    stars_count = sum(
        1 for m in menu
        if m.popularity_score >= avg_pop and (m.price - m.cost) >= avg_mar
    )

    def kpi_html(icon_class, icon_emoji, value, label):
        return (
            f'<div class="kpi-card">'
            f'<div class="kpi-icon {icon_class}">{icon_emoji}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'</div>'
        )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            kpi_html("kpi-icon-orange", "&#x1f4cb;", str(total_items), "TOTAL ITEMS"),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            kpi_html("kpi-icon-green", "&#x1f4b0;", fmt(avg_margin), "AVG MARGIN"),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            kpi_html("kpi-icon-red", "&#x1f4c9;", f"{avg_food_cost:.1f}%", "AVG FOOD COST %"),
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            kpi_html("kpi-icon-purple", "&#x2b50;", str(stars_count), "STARS COUNT"),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["Menu Items", "Menu Engineering", "Recommendations"])

    with tab1:
        show_menu_list(menu)
    with tab2:
        show_menu_engineering(menu)
    with tab3:
        show_recommendations(menu)


def show_menu_list(menu):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Current Menu Items</div>', unsafe_allow_html=True)

    cat_filter = st.selectbox("Category:", ["All", "appetizer", "main", "dessert", "beverage"])
    filtered = menu if cat_filter == "All" else [m for m in menu if m.category == cat_filter]

    table = []
    for item in filtered:
        margin = item.price - item.cost
        table.append({
            "Name": item.name,
            "Category": item.category.title(),
            f"Price ({currency_label()})": round(convert(item.price), 2),
            f"Cost ({currency_label()})": round(convert(item.cost), 2),
            f"Margin ({currency_label()})": round(convert(margin), 2),
            "Food Cost %": f"{item.food_cost_pct:.0f}%",
            "Popularity": f"{item.popularity_score * 100:.0f}%",
            "Avg Daily Orders": item.avg_daily_orders,
            "Prep Time (min)": item.prep_time_minutes,
        })
    st.dataframe(table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Margin by Item bar chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Margin by Item</div>', unsafe_allow_html=True)

    sorted_items = sorted(filtered, key=lambda m: m.price - m.cost, reverse=True)
    names = [m.name for m in sorted_items]
    margins = [round(m.price - m.cost, 1) for m in sorted_items]
    bar_colors = ["#28a745" if mg >= 20 else "#ffc107" if mg >= 10 else "#dc3545" for mg in margins]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names,
        y=margins,
        marker_color=bar_colors,
        marker_line=dict(width=0),
        text=[fmt(v) for v in margins],
        textposition="outside",
        textfont=dict(size=10),
    ))
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=10, b=80),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0", tickangle=-45),
        yaxis=dict(gridcolor="#f0f0f0", title=f"Margin ({currency_label()})"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Food Cost % by Item bar chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Food Cost % by Item</div>', unsafe_allow_html=True)

    sorted_fc = sorted(filtered, key=lambda m: m.food_cost_pct, reverse=True)
    fc_names = [m.name for m in sorted_fc]
    fc_vals = [round(m.food_cost_pct, 1) for m in sorted_fc]
    fc_colors = ["#dc3545" if v > 35 else "#ffc107" if v > 28 else "#28a745" for v in fc_vals]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=fc_names,
        y=fc_vals,
        marker_color=fc_colors,
        marker_line=dict(width=0),
        text=[f"{v}%" for v in fc_vals],
        textposition="outside",
        textfont=dict(size=10),
    ))
    fig2.add_hline(y=35, line_dash="dash", line_color="#dc3545",
                   annotation_text="35% Threshold", annotation_position="top right")
    fig2.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=10, b=80),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0", tickangle=-45),
        yaxis=dict(gridcolor="#f0f0f0", title="Food Cost %"),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_menu_engineering(menu):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Menu Engineering Matrix</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#636e72;font-size:0.9rem;margin-bottom:1rem;">'
        'Classify items by popularity and profitability (BCG-style analysis). '
        'Bubble size represents average daily orders.</p>',
        unsafe_allow_html=True,
    )

    avg_popularity = sum(m.popularity_score for m in menu) / len(menu)
    avg_margin = sum(m.price - m.cost for m in menu) / len(menu)

    stars, plowhorses, puzzles, dogs = [], [], [], []
    names, pops, margins, cats, sizes = [], [], [], [], []

    for item in menu:
        margin = item.price - item.cost
        pop = item.popularity_score
        names.append(item.name)
        pops.append(pop)
        margins.append(margin)
        cats.append(item.category)
        sizes.append(item.avg_daily_orders * 3)

        if pop >= avg_popularity and margin >= avg_margin:
            stars.append(item.name)
        elif pop >= avg_popularity and margin < avg_margin:
            plowhorses.append(item.name)
        elif pop < avg_popularity and margin >= avg_margin:
            puzzles.append(item.name)
        else:
            dogs.append(item.name)

    # Scatter plot
    color_map = {
        "appetizer": "#FF6B35",
        "main": "#2c3e50",
        "dessert": "#e83e8c",
        "beverage": "#17a2b8",
    }
    colors = [color_map.get(c, "#6c757d") for c in cats]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=margins,
        y=pops,
        mode="markers+text",
        text=names,
        textposition="top center",
        textfont=dict(size=9),
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.7,
            line=dict(width=1, color="white"),
        ),
    ))
    fig.add_hline(y=avg_popularity, line_dash="dash", line_color="gray",
                  annotation_text="Avg Popularity")
    fig.add_vline(x=avg_margin, line_dash="dash", line_color="gray",
                  annotation_text="Avg Margin")
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=f"Profit Margin ({currency_label()})",
        yaxis_title="Popularity Score",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0"),
        annotations=[
            dict(x=max(margins) * 0.85, y=max(pops) * 0.95, text="STARS",
                 showarrow=False, font=dict(size=14, color="green")),
            dict(x=min(margins) * 1.1, y=max(pops) * 0.95, text="PLOWHORSES",
                 showarrow=False, font=dict(size=14, color="orange")),
            dict(x=max(margins) * 0.85, y=min(pops) * 1.1, text="PUZZLES",
                 showarrow=False, font=dict(size=14, color="blue")),
            dict(x=min(margins) * 1.1, y=min(pops) * 1.1, text="DOGS",
                 showarrow=False, font=dict(size=14, color="red")),
        ],
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Quadrant summary cards ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Quadrant Summary</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        items_html = "".join(f'<div style="font-size:0.85rem;color:#636e72;padding:0.15rem 0;">{s}</div>' for s in stars)
        st.markdown(
            f'<div style="padding:0.5rem;">'
            f'<div style="font-weight:700;color:#28a745;font-size:0.95rem;margin-bottom:0.5rem;">Stars (Keep / Promote)</div>'
            f'<div style="font-size:1.5rem;font-weight:800;color:#2D3436;">{len(stars)}</div>'
            f'{items_html}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        items_html = "".join(f'<div style="font-size:0.85rem;color:#636e72;padding:0.15rem 0;">{s}</div>' for s in plowhorses)
        st.markdown(
            f'<div style="padding:0.5rem;">'
            f'<div style="font-weight:700;color:#ffc107;font-size:0.95rem;margin-bottom:0.5rem;">Plowhorses (Increase Price)</div>'
            f'<div style="font-size:1.5rem;font-weight:800;color:#2D3436;">{len(plowhorses)}</div>'
            f'{items_html}</div>',
            unsafe_allow_html=True,
        )
    with col3:
        items_html = "".join(f'<div style="font-size:0.85rem;color:#636e72;padding:0.15rem 0;">{s}</div>' for s in puzzles)
        st.markdown(
            f'<div style="padding:0.5rem;">'
            f'<div style="font-weight:700;color:#17a2b8;font-size:0.95rem;margin-bottom:0.5rem;">Puzzles (Promote / Reposition)</div>'
            f'<div style="font-size:1.5rem;font-weight:800;color:#2D3436;">{len(puzzles)}</div>'
            f'{items_html}</div>',
            unsafe_allow_html=True,
        )
    with col4:
        items_html = "".join(f'<div style="font-size:0.85rem;color:#636e72;padding:0.15rem 0;">{s}</div>' for s in dogs)
        st.markdown(
            f'<div style="padding:0.5rem;">'
            f'<div style="font-weight:700;color:#dc3545;font-size:0.95rem;margin-bottom:0.5rem;">Dogs (Consider Removing)</div>'
            f'<div style="font-size:1.5rem;font-weight:800;color:#2D3436;">{len(dogs)}</div>'
            f'{items_html}</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Category Breakdown chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Average Margin by Category</div>', unsafe_allow_html=True)

    cat_data = {}
    for m in menu:
        cat_data.setdefault(m.category, []).append(m.price - m.cost)
    cat_names = [c.title() for c in cat_data]
    cat_avg = [round(sum(v) / len(v), 1) for v in cat_data.values()]
    cat_colors = [color_map.get(c, "#6c757d") for c in cat_data]

    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(
        x=cat_names,
        y=cat_avg,
        marker_color=cat_colors,
        marker_line=dict(width=0),
        text=[fmt(v) for v in cat_avg],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig_cat.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0", title=f"Avg Margin ({currency_label()})"),
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_recommendations(menu):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Menu Recommendations</div>', unsafe_allow_html=True)

    # --- Food cost analysis ---
    high_cost = [m for m in menu if m.food_cost_pct > 35]
    if high_cost:
        st.markdown(
            f'<div class="alert-high">'
            f'<strong>{len(high_cost)} item{"s" if len(high_cost) != 1 else ""} with food cost above 35%</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )
        for item in high_cost:
            severity = "alert-critical" if item.food_cost_pct > 45 else "alert-high"
            st.markdown(
                f'<div class="{severity}">'
                f'<strong>{item.name}</strong> -- {item.food_cost_pct:.0f}% food cost<br>'
                f'<span style="font-size:0.85rem;color:#636e72;">'
                f'Consider renegotiating ingredient costs or adjusting portion size.</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # --- Low popularity items ---
    low_pop = [m for m in menu if m.popularity_score < 0.65 and m.is_active]
    if low_pop:
        st.markdown(
            f'<div class="alert-medium">'
            f'<strong>{len(low_pop)} item{"s" if len(low_pop) != 1 else ""} with low popularity (&lt;65%)</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )
        for item in low_pop:
            margin = item.price - item.cost
            if margin > 20:
                suggestion = f"High margin ({fmt(margin)}) but low demand. Try featuring as daily special."
                css_class = "alert-medium"
            else:
                suggestion = "Low margin and low demand. Consider removing or redesigning."
                css_class = "alert-critical"
            st.markdown(
                f'<div class="{css_class}">'
                f'<strong>{item.name}</strong> -- Popularity {item.popularity_score * 100:.0f}%<br>'
                f'<span style="font-size:0.85rem;color:#636e72;">{suggestion}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # --- Pricing opportunities ---
    avg_pop = sum(m.popularity_score for m in menu) / len(menu)
    avg_mar = sum(m.price - m.cost for m in menu) / len(menu)
    pricing_opp = [
        m for m in menu
        if m.popularity_score >= avg_pop and (m.price - m.cost) < avg_mar
    ]
    if pricing_opp:
        st.markdown(
            f'<div class="alert-low">'
            f'<strong>Pricing Opportunities</strong> -- '
            f'{len(pricing_opp)} popular item{"s" if len(pricing_opp) != 1 else ""} '
            f'with below-average margins may tolerate a price increase.'
            f'</div>',
            unsafe_allow_html=True,
        )
        for item in pricing_opp:
            margin = item.price - item.cost
            gap = avg_mar - margin
            st.markdown(
                f'<div class="alert-low">'
                f'<strong>{item.name}</strong> -- Margin {fmt(margin)} '
                f'({fmt(gap)} below average)<br>'
                f'<span style="font-size:0.85rem;color:#636e72;">'
                f'High popularity ({item.popularity_score * 100:.0f}%) suggests room for a price increase of {fmt(gap * 0.5)}-{fmt(gap)}.</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)

    # --- Top Performers ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top Performers</div>', unsafe_allow_html=True)

    top = sorted(menu, key=lambda m: (m.price - m.cost) * m.avg_daily_orders, reverse=True)[:5]
    for i, item in enumerate(top):
        daily_profit = (item.price - item.cost) * item.avg_daily_orders
        margin = item.price - item.cost
        st.markdown(
            f'<div class="insight-card">'
            f'<div class="insight-title">#{i + 1} {item.name}</div>'
            f'<div class="insight-desc">'
            f'Daily profit contribution: <strong>{fmt(daily_profit)}</strong> '
            f'| Margin: {fmt(margin)} | Orders/day: {item.avg_daily_orders}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Contribution Breakdown Chart ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Daily Profit Contribution (All Items)</div>', unsafe_allow_html=True)

    sorted_menu = sorted(menu, key=lambda m: (m.price - m.cost) * m.avg_daily_orders, reverse=True)
    contrib_names = [m.name for m in sorted_menu]
    contrib_vals = [round((m.price - m.cost) * m.avg_daily_orders, 0) for m in sorted_menu]
    contrib_colors = [
        "#28a745" if v >= 100 else "#ffc107" if v >= 50 else "#dc3545"
        for v in contrib_vals
    ]

    fig_contrib = go.Figure()
    fig_contrib.add_trace(go.Bar(
        x=contrib_names,
        y=contrib_vals,
        marker_color=contrib_colors,
        marker_line=dict(width=0),
        text=[fmt(v) for v in contrib_vals],
        textposition="outside",
        textfont=dict(size=10),
    ))
    fig_contrib.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=10, b=100),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f0f0f0", tickangle=-45),
        yaxis=dict(gridcolor="#f0f0f0", title=f"Daily Profit ({currency_label()})"),
    )
    st.plotly_chart(fig_contrib, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
