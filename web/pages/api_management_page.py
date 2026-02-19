"""API Management Page - POS integration, keys, and endpoint documentation"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import API_MANAGEMENT_HEADER_SVG, render_svg

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


def _api_post(path, json_data=None):
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
    st.markdown(render_svg(API_MANAGEMENT_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Manage API keys, view endpoint documentation, '
        'and monitor POS integration status.</p>',
        unsafe_allow_html=True,
    )

    # API Status
    health = _api_get("/api/v1/health")
    api_online = health is not None

    if api_online:
        st.markdown(
            f'<div style="display:flex;gap:1rem;align-items:center;margin-bottom:1rem;">'
            f'<span class="badge badge-normal">API Online</span>'
            f'<span style="color:#636e72;font-size:0.85rem;">'
            f'v{health.get("version","?")} | DB: {health.get("database","?")} | '
            f'Uptime: {health.get("uptime_seconds",0):.0f}s</span>'
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
            '<code>cd C:\\Users\\Administrator\\forkast_platform && python -m api.main</code>'
            '</div>',
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3 = st.tabs(["API Keys", "Endpoints", "POS Integration Guide"])

    # --- Tab 1: API Keys ---
    with tab1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Generate API Key</div>', unsafe_allow_html=True)

        with st.form("generate_key"):
            c1, c2 = st.columns(2)
            with c1:
                key_name = st.text_input("Key Name", placeholder="My POS System")
            with c2:
                perms = st.multiselect(
                    "Permissions",
                    ["pos:read", "pos:write", "payments:read", "payments:write"],
                    default=["pos:read", "pos:write"],
                )
            gen_submitted = st.form_submit_button("Generate Key", type="primary")

        if gen_submitted and api_online:
            if not key_name.strip():
                st.error("Key name is required.")
            else:
                from api.database import SessionLocal
                from api.services.data_service import DataService
                db = SessionLocal()
                try:
                    db_key, raw_key = DataService.create_api_key(
                        db, key_name.strip(), permissions=perms
                    )
                    st.success("API key generated successfully!")
                    st.code(raw_key, language=None)
                    st.markdown(
                        '<div class="alert-high">'
                        '<strong>Save this key now!</strong> It will not be shown again.'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                finally:
                    db.close()

        st.markdown('</div>', unsafe_allow_html=True)

        # List existing keys
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Active API Keys</div>', unsafe_allow_html=True)

        if api_online:
            from api.database import SessionLocal
            from api.services.data_service import DataService
            db = SessionLocal()
            try:
                keys = DataService.list_api_keys(db)
                if keys:
                    table = []
                    for k in keys:
                        table.append({
                            "ID": k.id,
                            "Prefix": k.key_prefix,
                            "Name": k.name,
                            "Permissions": ", ".join(k.permissions or []),
                            "Active": "Yes" if k.is_active else "No",
                            "Requests": k.request_count,
                            "Created": k.created_at.strftime("%Y-%m-%d %H:%M") if k.created_at else "",
                            "Last Used": k.last_used_at.strftime("%Y-%m-%d %H:%M") if k.last_used_at else "Never",
                        })
                    st.dataframe(table, use_container_width=True)

                    # Revoke
                    revoke_id = st.number_input("Revoke Key ID", min_value=1, step=1, value=1)
                    if st.button("Revoke Key"):
                        if DataService.revoke_api_key(db, revoke_id):
                            st.success(f"Key {revoke_id} revoked.")
                            st.rerun()
                        else:
                            st.error("Key not found.")
                else:
                    st.markdown(
                        '<p style="color:#636e72;text-align:center;padding:1rem;">No API keys generated yet.</p>',
                        unsafe_allow_html=True,
                    )
            finally:
                db.close()

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Tab 2: Endpoints ---
    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">API Endpoints</div>', unsafe_allow_html=True)

        if api_online:
            st.markdown(
                f'<div class="alert-low">'
                f'<strong>Interactive Docs:</strong> '
                f'<a href="{API_BASE}/docs" target="_blank">{API_BASE}/docs</a> (Swagger UI) | '
                f'<a href="{API_BASE}/redoc" target="_blank">{API_BASE}/redoc</a> (ReDoc)'
                f'</div>',
                unsafe_allow_html=True,
            )

        endpoints = [
            ("POST", "/api/v1/pos/orders", "Submit order from POS", "pos:write"),
            ("GET", "/api/v1/pos/orders", "List orders (date filters, pagination)", "pos:read"),
            ("GET", "/api/v1/pos/orders/{uid}", "Get single order", "pos:read"),
            ("POST", "/api/v1/pos/menu/sync", "Sync menu items (upsert by name)", "pos:write"),
            ("GET", "/api/v1/pos/menu", "Get current menu", "pos:read"),
            ("PUT", "/api/v1/pos/menu/{uid}", "Update menu item", "pos:write"),
            ("POST", "/api/v1/pos/inventory/update", "Batch update inventory", "pos:write"),
            ("GET", "/api/v1/pos/inventory", "Get current inventory", "pos:read"),
            ("POST", "/api/v1/pos/staff/clock-in", "Staff clock-in", "pos:write"),
            ("POST", "/api/v1/pos/staff/clock-out", "Staff clock-out", "pos:write"),
            ("GET", "/api/v1/pos/staff/schedule", "Get clock events", "pos:read"),
            ("GET", "/api/v1/pos/forecasts", "Get demand forecasts", "pos:read"),
            ("POST", "/api/v1/payments/create-checkout", "Create Stripe checkout", "payments:write"),
            ("POST", "/api/v1/payments/webhook", "Stripe webhook", "Stripe sig"),
            ("GET", "/api/v1/payments", "List payments", "payments:read"),
            ("GET", "/api/v1/payments/stats", "Payment statistics", "payments:read"),
            ("GET", "/api/v1/payments/{uid}", "Get payment details", "payments:read"),
            ("POST", "/api/v1/payments/{uid}/refund", "Refund payment", "payments:write"),
            ("GET", "/api/v1/health", "Health check", "None"),
            ("GET", "/api/v1/info", "API info", "None"),
        ]

        table = [{"Method": m, "Path": p, "Description": d, "Auth": a} for m, p, d, a in endpoints]
        st.dataframe(table, use_container_width=True, height=600)

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Tab 3: POS Integration Guide ---
    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">POS Integration Guide</div>', unsafe_allow_html=True)

        st.markdown("""
**Authentication:** All POS endpoints require an `X-API-Key` header.

**Base URL:** `http://localhost:8518`

---

**1. Submit an Order**
```bash
curl -X POST http://localhost:8518/api/v1/pos/orders \\
  -H "X-API-Key: YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "restaurant_uid": "RESTAURANT_UID",
    "channel": "dine_in",
    "items": [
      {"item_name": "Hummus", "quantity": 2, "unit_price": 15.0},
      {"item_name": "Grilled Chicken", "quantity": 1, "unit_price": 45.0}
    ],
    "covers": 2,
    "table_number": 5,
    "pos_reference": "POS-12345"
  }'
```

**2. Sync Menu Items**
```bash
curl -X POST http://localhost:8518/api/v1/pos/menu/sync \\
  -H "X-API-Key: YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "restaurant_uid": "RESTAURANT_UID",
    "items": [
      {"name": "Hummus", "category": "appetizer", "price": 15.0, "cost": 4.5},
      {"name": "Grilled Chicken", "category": "main", "price": 45.0, "cost": 15.0}
    ]
  }'
```

**3. Update Inventory**
```bash
curl -X POST http://localhost:8518/api/v1/pos/inventory/update \\
  -H "X-API-Key: YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "restaurant_uid": "RESTAURANT_UID",
    "items": [
      {"name": "Chicken Breast", "new_stock": 45.5, "unit": "kg"},
      {"name": "Rice Basmati", "new_stock": 80.0}
    ]
  }'
```

**4. Staff Clock-In**
```bash
curl -X POST http://localhost:8518/api/v1/pos/staff/clock-in \\
  -H "X-API-Key: YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "restaurant_uid": "RESTAURANT_UID",
    "staff_name": "Ahmed Hassan",
    "role": "chef"
  }'
```

**5. Get Demand Forecasts**
```bash
curl http://localhost:8518/api/v1/pos/forecasts?restaurant_uid=RESTAURANT_UID&days_ahead=7 \\
  -H "X-API-Key: YOUR_API_KEY"
```
""")

        st.markdown('</div>', unsafe_allow_html=True)
