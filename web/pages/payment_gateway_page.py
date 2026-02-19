"""Payment Gateway Page - Stripe-powered payment dashboard"""
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import PAYMENT_GATEWAY_HEADER_SVG, render_svg
from web.utils.currency import fmt, currency_label, convert

API_BASE = "http://localhost:8518"
ADMIN_KEY = "fk-admin-dev-key-change-me"


def _api_get(path, params=None):
    """Call FastAPI GET endpoint."""
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


def _api_post(path, json_data=None):
    """Call FastAPI POST endpoint."""
    import httpx
    try:
        r = httpx.post(
            f"{API_BASE}{path}",
            headers={"X-API-Key": ADMIN_KEY},
            json=json_data,
            timeout=5.0,
        )
        return r.status_code, r.json()
    except Exception as e:
        return None, str(e)


def show():
    st.markdown(render_svg(PAYMENT_GATEWAY_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Monitor payment transactions, manage Stripe integration, '
        'and track procurement payments.</p>',
        unsafe_allow_html=True,
    )

    # Check API status
    health = _api_get("/api/v1/health")
    api_online = health is not None

    if api_online:
        stripe_status = health.get("stripe", "not_configured")
        stripe_ok = stripe_status == "configured"
        status_color = "#28a745" if stripe_ok else "#ffc107"
        status_text = "Connected" if stripe_ok else "Not Configured"

        st.markdown(
            f'<div style="display:flex;gap:1rem;align-items:center;margin-bottom:1rem;">'
            f'<span class="badge badge-normal">API Online</span>'
            f'<span class="badge" style="background:{status_color};color:white;">Stripe: {status_text}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            "FastAPI backend is not running. Start it with: "
            "`python -m api.main` (from the project root)"
        )
        st.markdown(
            '<div class="alert-medium">'
            '<strong>Quick Start</strong><br>'
            'Run the API server alongside Streamlit:<br>'
            '<code>cd C:\\Users\\Administrator\\forkast_platform && python -m api.main</code>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    # --- Payment Stats ---
    stats = _api_get("/api/v1/payments/stats") or {
        "total_processed": 0, "total_refunded": 0, "total_pending": 0,
        "count_succeeded": 0, "count_failed": 0, "count_pending": 0, "count_refunded": 0,
    }

    col1, col2, col3, col4, col5 = st.columns(5)

    def kpi_html(icon_class, icon_emoji, value, label):
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_emoji}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>'''

    with col1:
        st.markdown(kpi_html(
            "kpi-icon-green", "💰",
            fmt(stats["total_processed"]),
            "TOTAL PROCESSED",
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_html(
            "kpi-icon-purple", "🏢",
            fmt(stats.get("total_forkast_revenue", 0)),
            "FORKAST REVENUE",
        ), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_html(
            "kpi-icon-orange", "⏳",
            fmt(stats["total_pending"]),
            "PENDING",
        ), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_html(
            "kpi-icon-red", "↩️",
            fmt(stats["total_refunded"]),
            "REFUNDED",
        ), unsafe_allow_html=True)
    with col5:
        total_tx = stats["count_succeeded"] + stats["count_failed"] + stats["count_pending"] + stats["count_refunded"]
        st.markdown(kpi_html(
            "kpi-icon-blue", "📊",
            str(total_tx),
            "TOTAL TRANSACTIONS",
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Charts + Transactions ---
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Payment Status</div>', unsafe_allow_html=True)

        labels = ["Succeeded", "Pending", "Failed", "Refunded"]
        values = [
            stats["count_succeeded"], stats["count_pending"],
            stats["count_failed"], stats["count_refunded"],
        ]
        colors = ["#28a745", "#ffc107", "#dc3545", "#17a2b8"]

        if sum(values) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=labels, values=values,
                marker_colors=colors,
                hole=0.5,
                textinfo="label+value",
                textfont=dict(size=12),
            )])
            fig.update_layout(
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                '<p style="text-align:center;color:#636e72;padding:3rem 0;">'
                'No transactions yet</p>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recent Transactions</div>', unsafe_allow_html=True)

        payments = _api_get("/api/v1/payments", {"limit": 20}) or []

        if payments:
            table = []
            for p in payments:
                table.append({
                    "UID": p["uid"],
                    f"Total ({currency_label()})": round(convert(p["amount"]), 2),
                    f"Supplier ({currency_label()})": round(convert(p.get("supplier_amount", 0)), 2),
                    f"Fee ({currency_label()})": round(convert(p.get("forkast_fee", 0)), 2),
                    "Fee %": f'{p.get("forkast_fee_pct", 15.0):.0f}%',
                    "Status": p["status"].title(),
                    "Description": p.get("description", "")[:30],
                    "Date": p["created_at"][:16].replace("T", " "),
                })
            st.dataframe(table, use_container_width=True)
        else:
            st.markdown(
                '<p style="text-align:center;color:#636e72;padding:2rem 0;">'
                'No payment transactions yet. Create a test payment below.</p>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Create Test Payment ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Create Test Payment</div>', unsafe_allow_html=True)

    if not stripe_ok:
        st.markdown(
            '<div class="alert-medium">'
            '<strong>Stripe Not Configured</strong><br>'
            'Set <code>FORKAST_STRIPE_SECRET_KEY</code> environment variable to enable payments. '
            'Use a Stripe test key (<code>sk_test_...</code>) for testing.'
            '</div>',
            unsafe_allow_html=True,
        )

    with st.form("test_payment"):
        c1, c2, c3 = st.columns(3)
        with c1:
            supplier_amount = st.number_input("Supplier Amount (AED)", min_value=1.0, value=100.0, step=10.0)
        with c2:
            currency = st.selectbox("Currency", ["aed", "usd", "kwd"])
        with c3:
            desc = st.text_input("Description", value="Test procurement payment")

        # Show fee preview
        fee_preview = round(supplier_amount * 0.15, 2)
        total_preview = round(supplier_amount + fee_preview, 2)
        st.markdown(
            f'<div style="background:#f8f9fa;border-radius:8px;padding:0.8rem 1rem;margin:0.5rem 0;">'
            f'<strong>Fee Breakdown:</strong> '
            f'Supplier: <strong>AED {supplier_amount:,.2f}</strong> + '
            f'Forkast Fee (15%): <strong>AED {fee_preview:,.2f}</strong> = '
            f'Restaurant Pays: <strong>AED {total_preview:,.2f}</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button("Create Checkout Session", type="primary")

    if submitted:
        rest_uid = st.session_state.restaurant.uid if hasattr(st.session_state, "restaurant") else "demo"
        status, result = _api_post("/api/v1/payments/create-checkout", {
            "restaurant_uid": rest_uid,
            "amount": supplier_amount,
            "currency": currency,
            "description": desc,
        })
        if status == 201:
            st.success(
                f"Payment created: {result.get('uid', 'N/A')} | "
                f"Total: AED {result.get('amount', 0):,.2f} | "
                f"Supplier: AED {result.get('supplier_amount', 0):,.2f} | "
                f"Forkast Fee: AED {result.get('forkast_fee', 0):,.2f}"
            )
        elif status == 503:
            st.error("Stripe not configured. Set FORKAST_STRIPE_SECRET_KEY.")
        else:
            st.error(f"Error: {result}")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- Stripe Configuration Guide ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Stripe Configuration</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="padding:0.5rem 0;font-size:0.9rem;color:#636e72;">'
        '<strong>Environment Variables:</strong><br>'
        '<code>FORKAST_STRIPE_SECRET_KEY</code> - Your Stripe secret key (sk_test_... or sk_live_...)<br>'
        '<code>FORKAST_STRIPE_WEBHOOK_SECRET</code> - Webhook signing secret (whsec_...)<br>'
        '<code>FORKAST_STRIPE_PUBLISHABLE_KEY</code> - Publishable key (pk_test_... or pk_live_...)<br>'
        '<br><strong>Webhook URL:</strong><br>'
        f'<code>{API_BASE}/api/v1/payments/webhook</code>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
