"""Loyalty Program Page - Tier-based rewards for restaurant-supplier relationships"""
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import LOYALTY_HEADER_SVG, render_svg
from web.utils.currency import fmt, currency_label, convert

API_BASE = "http://localhost:8518"
ADMIN_KEY = "fk-admin-dev-key-change-me"

TIER_COLORS = {
    "standard": "#636e72",
    "bronze": "#CD7F32",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "platinum": "#E5E4E2",
}

TIER_BG = {
    "standard": "rgba(99,110,114,0.1)",
    "bronze": "rgba(205,127,50,0.12)",
    "silver": "rgba(192,192,192,0.12)",
    "gold": "rgba(255,215,0,0.12)",
    "platinum": "rgba(229,228,226,0.15)",
}


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
    st.markdown(render_svg(LOYALTY_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Earn loyalty tiers with your suppliers through consistent ordering. '
        'Higher tiers mean lower Forkast fees - saving you money on every transaction.</p>',
        unsafe_allow_html=True,
    )

    # Check API status
    health = _api_get("/api/v1/health")
    if not health:
        st.warning("FastAPI backend is not running. Start it with: `python -m api.main`")
        return

    rest_uid = st.session_state.restaurant.uid if hasattr(st.session_state, "restaurant") else None
    if not rest_uid:
        st.warning("No restaurant loaded in session.")
        return

    # --- Tier Explanation ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Loyalty Tier Ladder</div>', unsafe_allow_html=True)

    tiers = _api_get("/api/v1/loyalty/tiers") or []

    if tiers:
        cols = st.columns(len(tiers))
        for i, (col, tier) in enumerate(zip(cols, tiers)):
            with col:
                color = TIER_COLORS.get(tier["name"], "#636e72")
                bg = TIER_BG.get(tier["name"], "rgba(0,0,0,0.05)")
                arrow = "&#9650;" if i > 0 else ""
                st.markdown(
                    f'<div style="background:{bg};border:2px solid {color};border-radius:12px;'
                    f'padding:1rem;text-align:center;">'
                    f'<div style="font-size:0.7rem;color:#636e72;text-transform:uppercase;letter-spacing:1px;">'
                    f'{tier["min_orders"]}+ orders</div>'
                    f'<div style="font-size:1.3rem;font-weight:800;color:{color};margin:0.3rem 0;">'
                    f'{tier["name"].title()}</div>'
                    f'<div style="font-size:0.85rem;color:#2D3436;">'
                    f'Fee: <strong>{tier["effective_fee"]}%</strong></div>'
                    f'<div style="font-size:0.8rem;color:#28a745;font-weight:600;">'
                    f'{"Save " + str(tier["discount_pct"]) + "%" if tier["discount_pct"] > 0 else "Base rate"}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Fetch Loyalty Summary ---
    summary = _api_get("/api/v1/loyalty/summary", {"restaurant_uid": rest_uid})

    if not summary or summary["total_supplier_accounts"] == 0:
        st.markdown(
            '<div class="section-card">'
            '<p style="text-align:center;color:#636e72;padding:2rem 0;">'
            'No loyalty accounts yet. Loyalty accounts are created automatically '
            'when you make payments to suppliers via the Payment Gateway.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    # --- Summary KPIs ---
    def kpi_html(icon_class, icon_emoji, value, label):
        return f'''<div class="kpi-card">
            <div class="kpi-icon {icon_class}">{icon_emoji}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>'''

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_html(
            "kpi-icon-orange", "🏭",
            str(summary["total_supplier_accounts"]),
            "SUPPLIER ACCOUNTS",
        ), unsafe_allow_html=True)
    with c2:
        # Count non-standard tiers
        active = sum(v for k, v in summary["active_tiers"].items() if k != "standard")
        st.markdown(kpi_html(
            "kpi-icon-green", "🎖️",
            str(active),
            "ACTIVE TIERS",
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_html(
            "kpi-icon-purple", "💰",
            fmt(summary["total_savings"]),
            "TOTAL SAVINGS",
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_html(
            "kpi-icon-blue", "📊",
            f'{summary["avg_discount_pct"]:.1f}%',
            "AVG DISCOUNT",
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Tier Distribution Chart + Supplier Cards ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Tier Distribution</div>', unsafe_allow_html=True)

        tier_data = summary["active_tiers"]
        if tier_data:
            labels = list(tier_data.keys())
            values = list(tier_data.values())
            colors = [TIER_COLORS.get(t, "#636e72") for t in labels]

            fig = go.Figure(data=[go.Pie(
                labels=[t.title() for t in labels],
                values=values,
                marker_colors=colors,
                hole=0.5,
                textinfo="label+value",
                textfont=dict(size=11),
            )])
            fig.update_layout(
                height=280, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Supplier Loyalty Status</div>', unsafe_allow_html=True)

        accounts = summary.get("accounts", [])
        for acct in accounts:
            tier = acct["current_tier"]
            color = TIER_COLORS.get(tier, "#636e72")
            bg = TIER_BG.get(tier, "rgba(0,0,0,0.05)")

            # Progress bar toward next tier
            progress_html = ""
            if acct.get("next_tier") and acct.get("orders_to_next_tier") is not None:
                next_t = acct["next_tier"]
                orders_to_next = acct["orders_to_next_tier"]
                # Find the next tier's min_orders
                next_min = 0
                current_min = 0
                for t in (tiers or []):
                    if t["name"] == next_t:
                        next_min = t["min_orders"]
                    if t["name"] == tier:
                        current_min = t["min_orders"]
                range_size = next_min - current_min if next_min > current_min else 1
                progress = ((acct["orders_90d"] - current_min) / range_size) * 100
                progress = max(0, min(100, progress))

                progress_html = (
                    f'<div style="margin-top:0.5rem;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#636e72;">'
                    f'<span>{acct["orders_90d"]} orders (90d)</span>'
                    f'<span>{orders_to_next} more to {next_t.title()}</span></div>'
                    f'<div style="background:#e9ecef;border-radius:6px;height:8px;margin-top:4px;">'
                    f'<div style="background:{color};border-radius:6px;height:8px;width:{progress:.0f}%;'
                    f'transition:width 0.3s;"></div></div></div>'
                )
            elif not acct.get("next_tier"):
                progress_html = (
                    f'<div style="margin-top:0.5rem;font-size:0.75rem;color:#28a745;font-weight:600;">'
                    f'Maximum tier reached! {acct["orders_90d"]} orders (90d)</div>'
                )

            st.markdown(
                f'<div style="background:{bg};border-left:4px solid {color};border-radius:8px;'
                f'padding:1rem;margin-bottom:0.8rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div>'
                f'<span style="font-weight:700;font-size:1rem;color:#2D3436;">'
                f'{acct.get("supplier_name", acct["supplier_uid"])}</span>'
                f'<span style="display:inline-block;background:{color};color:white;'
                f'padding:2px 10px;border-radius:12px;font-size:0.7rem;font-weight:700;'
                f'margin-left:0.5rem;">{tier.title()}</span>'
                f'</div>'
                f'<div style="text-align:right;">'
                f'<div style="font-size:0.8rem;color:#636e72;">Fee: <strong>{acct["effective_fee"]}%</strong>'
                f'{" (Save " + str(acct["discount_pct"]) + "%)" if acct["discount_pct"] > 0 else ""}</div>'
                f'<div style="font-size:0.75rem;color:#636e72;">'
                f'Lifetime: {acct["total_orders"]} orders | {fmt(acct["total_spent"])}</div>'
                f'</div></div>'
                f'{progress_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Transaction History ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Loyalty Activity Log</div>', unsafe_allow_html=True)

    # Get history for all accounts
    all_history = []
    for acct in accounts:
        history = _api_get(
            f"/api/v1/loyalty/accounts/{acct['supplier_uid']}/history",
            {"restaurant_uid": rest_uid, "limit": 20}
        ) or []
        for h in history:
            h["supplier_name"] = acct.get("supplier_name", acct["supplier_uid"])
        all_history.extend(history)

    # Sort by date descending
    all_history.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    if all_history:
        table = []
        event_icons = {
            "payment_completed": "💳",
            "tier_upgrade": "⬆️",
            "tier_downgrade": "⬇️",
            "decay_check": "🔄",
        }
        for h in all_history[:30]:
            icon = event_icons.get(h["event_type"], "📝")
            table.append({
                "Event": f'{icon} {h["event_type"].replace("_", " ").title()}',
                "Supplier": h.get("supplier_name", ""),
                "Tier": f'{h["old_tier"].title()} -> {h["new_tier"].title()}' if h["old_tier"] != h["new_tier"] else h["new_tier"].title(),
                f"Amount ({currency_label()})": round(convert(h["amount"]), 2) if h["amount"] > 0 else "",
                f"Saved ({currency_label()})": round(convert(h["discount_applied"]), 2) if h["discount_applied"] > 0 else "",
                "Orders (90d)": h["order_count"],
                "Date": h["created_at"][:16].replace("T", " "),
            })
        st.dataframe(table, use_container_width=True, height=400)
    else:
        st.markdown(
            '<p style="text-align:center;color:#636e72;padding:2rem 0;">'
            'No loyalty events recorded yet.</p>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
