"""Revenue Model Page - Forkast revenue generation from supplier-restaurant transactions"""
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import REVENUE_MODEL_HEADER_SVG, render_svg
from web.utils.currency import fmt, currency_label, convert

API_BASE = "http://localhost:8518"
ADMIN_KEY = "fk-admin-dev-key-change-me"


def _api_get(path, params=None):
    import httpx
    try:
        r = httpx.get(
            f"{API_BASE}{path}",
            headers={"X-API-Key": ADMIN_KEY},
            params=params,
            timeout=5.0,
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def show():
    st.markdown(render_svg(REVENUE_MODEL_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Track Forkast platform revenue from the 15% transaction fee '
        'on every supplier-restaurant payment.</p>',
        unsafe_allow_html=True,
    )

    # Check API status
    health = _api_get("/api/v1/health")
    api_online = health is not None

    if not api_online:
        st.warning(
            "FastAPI backend is not running. Start it with: "
            "`python -m api.main` (from the project root)"
        )
        return

    # Fetch revenue data
    revenue = _api_get("/api/v1/payments/revenue") or {
        "total_transactions": 0, "total_volume": 0, "total_forkast_revenue": 0,
        "total_supplier_payouts": 0, "avg_fee_pct": 15.0,
        "avg_transaction_size": 0, "revenue_by_status": {}, "recent_transactions": [],
    }

    # --- Revenue Model Explanation ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Forkast Revenue Model</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap;">'
        '<div style="flex:1;min-width:200px;">'
        '<div style="background:linear-gradient(135deg,#f0f9ff,#bee3f8);border-radius:12px;padding:1.2rem;text-align:center;">'
        '<div style="font-size:0.8rem;color:#636e72;text-transform:uppercase;letter-spacing:1px;">Supplier Invoice</div>'
        '<div style="font-size:1.5rem;font-weight:800;color:#2D3436;">Base Amount</div>'
        '</div></div>'
        '<div style="font-size:2rem;color:#FF6B35;font-weight:800;">+</div>'
        '<div style="flex:1;min-width:200px;">'
        '<div style="background:linear-gradient(135deg,#fff5f0,#fed7aa);border-radius:12px;padding:1.2rem;text-align:center;">'
        '<div style="font-size:0.8rem;color:#636e72;text-transform:uppercase;letter-spacing:1px;">Forkast Fee</div>'
        '<div style="font-size:1.5rem;font-weight:800;color:#FF6B35;">15%</div>'
        '</div></div>'
        '<div style="font-size:2rem;color:#28a745;font-weight:800;">=</div>'
        '<div style="flex:1;min-width:200px;">'
        '<div style="background:linear-gradient(135deg,#f0fff4,#c6f6d5);border-radius:12px;padding:1.2rem;text-align:center;">'
        '<div style="font-size:0.8rem;color:#636e72;text-transform:uppercase;letter-spacing:1px;">Restaurant Pays</div>'
        '<div style="font-size:1.5rem;font-weight:800;color:#28a745;">Total</div>'
        '</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KPI Cards ---
    c1, c2, c3, c4 = st.columns(4)

    def kpi_html(icon_class, icon_emoji, value, label):
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_emoji}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>'''

    with c1:
        st.markdown(kpi_html(
            "kpi-icon-purple", "🏢",
            fmt(revenue["total_forkast_revenue"]),
            "FORKAST REVENUE",
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_html(
            "kpi-icon-green", "💰",
            fmt(revenue["total_volume"]),
            "TOTAL VOLUME",
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_html(
            "kpi-icon-blue", "🏭",
            fmt(revenue["total_supplier_payouts"]),
            "SUPPLIER PAYOUTS",
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_html(
            "kpi-icon-orange", "📊",
            str(revenue["total_transactions"]),
            "TRANSACTIONS",
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Charts ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Revenue Split</div>', unsafe_allow_html=True)

        forkast_rev = revenue["total_forkast_revenue"]
        supplier_pay = revenue["total_supplier_payouts"]

        if forkast_rev > 0 or supplier_pay > 0:
            fig = go.Figure(data=[go.Pie(
                labels=["Forkast Revenue (15%)", "Supplier Payouts (85%)"],
                values=[forkast_rev, supplier_pay],
                marker_colors=["#FF6B35", "#28a745"],
                hole=0.55,
                textinfo="label+percent",
                textfont=dict(size=11),
            )])
            fig.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                annotations=[dict(
                    text=f"<b>{fmt(forkast_rev)}</b><br>Revenue",
                    x=0.5, y=0.5, font_size=14, showarrow=False,
                    font=dict(color="#FF6B35"),
                )],
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                '<p style="text-align:center;color:#636e72;padding:3rem 0;">'
                'No revenue data yet. Create transactions via Payment Gateway.</p>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Revenue by Status</div>', unsafe_allow_html=True)

        rev_status = revenue.get("revenue_by_status", {})
        if rev_status:
            status_colors = {
                "succeeded": "#28a745", "pending": "#ffc107",
                "failed": "#dc3545", "refunded": "#17a2b8",
                "processing": "#FF6B35",
            }
            fig = go.Figure(data=[go.Bar(
                x=list(rev_status.keys()),
                y=[convert(v) for v in rev_status.values()],
                marker_color=[status_colors.get(s, "#636e72") for s in rev_status.keys()],
                text=[fmt(v) for v in rev_status.values()],
                textposition="outside",
            )])
            fig.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=30),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title=""), yaxis=dict(title=f"Fee Revenue ({currency_label()})"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                '<p style="text-align:center;color:#636e72;padding:3rem 0;">'
                'No status breakdown yet.</p>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Transaction Ledger ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Transaction Fee Ledger</div>', unsafe_allow_html=True)

    transactions = revenue.get("recent_transactions", [])
    if transactions:
        table = []
        for tx in transactions:
            table.append({
                "UID": tx["uid"],
                f"Total ({currency_label()})": round(convert(tx["amount"]), 2),
                f"Supplier ({currency_label()})": round(convert(tx["supplier_amount"]), 2),
                f"Forkast Fee ({currency_label()})": round(convert(tx["forkast_fee"]), 2),
                "Fee %": f'{tx["forkast_fee_pct"]:.0f}%',
                "Status": tx["status"].title(),
                "Description": tx["description"][:35],
                "Date": tx["created_at"][:16].replace("T", " "),
            })
        st.dataframe(table, use_container_width=True, height=400)
    else:
        st.markdown(
            '<p style="text-align:center;color:#636e72;padding:2rem 0;">'
            'No transactions recorded yet. Use Payment Gateway to create test payments.</p>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # --- Revenue Projections ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Revenue Projection Calculator</div>', unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        monthly_restaurants = st.number_input(
            "Active Restaurants", min_value=1, value=50, step=10
        )
    with pc2:
        avg_monthly_volume = st.number_input(
            "Avg Monthly Volume per Restaurant (AED)", min_value=1000, value=50000, step=5000
        )
    with pc3:
        fee_pct = st.number_input(
            "Platform Fee %", min_value=1.0, max_value=30.0, value=15.0, step=0.5
        )

    monthly_volume = monthly_restaurants * avg_monthly_volume
    monthly_revenue = monthly_volume * fee_pct / 100
    annual_revenue = monthly_revenue * 12

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(kpi_html(
            "kpi-icon-blue", "🏪",
            str(monthly_restaurants),
            "RESTAURANTS",
        ), unsafe_allow_html=True)
    with mc2:
        st.markdown(kpi_html(
            "kpi-icon-green", "💰",
            f"AED {monthly_volume:,.0f}",
            "MONTHLY VOLUME",
        ), unsafe_allow_html=True)
    with mc3:
        st.markdown(kpi_html(
            "kpi-icon-purple", "🏢",
            f"AED {monthly_revenue:,.0f}",
            "MONTHLY REVENUE",
        ), unsafe_allow_html=True)
    with mc4:
        st.markdown(kpi_html(
            "kpi-icon-orange", "📈",
            f"AED {annual_revenue:,.0f}",
            "ANNUAL REVENUE",
        ), unsafe_allow_html=True)

    # Growth chart
    months = list(range(1, 13))
    growth_rates = [0.05, 0.08, 0.10, 0.12, 0.10, 0.08, 0.10, 0.12, 0.08, 0.10, 0.08, 0.06]
    cumulative_restaurants = [monthly_restaurants]
    for g in growth_rates[:-1]:
        cumulative_restaurants.append(int(cumulative_restaurants[-1] * (1 + g)))

    projected_revenue = [r * avg_monthly_volume * fee_pct / 100 for r in cumulative_restaurants]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"M{m}" for m in months],
        y=projected_revenue,
        marker_color="#FF6B35",
        name="Monthly Revenue",
        text=[f"AED {v:,.0f}" for v in projected_revenue],
        textposition="outside",
    ))
    fig.add_trace(go.Scatter(
        x=[f"M{m}" for m in months],
        y=cumulative_restaurants,
        mode="lines+markers",
        name="Restaurants",
        yaxis="y2",
        line=dict(color="#28a745", width=3),
        marker=dict(size=8),
    ))
    fig.update_layout(
        height=350, margin=dict(l=10, r=60, t=30, b=30),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title=""),
        yaxis=dict(title="Revenue (AED)", side="left"),
        yaxis2=dict(title="Restaurants", side="right", overlaying="y"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
