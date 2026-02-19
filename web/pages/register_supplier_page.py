"""Register Supplier Page"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from web.assets.images import REGISTER_SUPPLIER_HEADER_SVG, render_svg
from models.core import Supplier, SupplierTier, IngredientCategory


def show():
    st.markdown(render_svg(REGISTER_SUPPLIER_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown(
        '<p class="page-desc">Join the Forkast supplier network to gain demand visibility '
        'and connect with MENA restaurants.</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Supplier Details</div>', unsafe_allow_html=True)

    with st.form("register_supplier", clear_on_submit=False):
        # Row 1: Name, Tier
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Supplier Name *")
        with c2:
            tier = st.selectbox(
                "Tier *",
                options=[t for t in SupplierTier],
                format_func=lambda t: t.value.title(),
            )

        # Row 2: Categories
        categories = st.multiselect(
            "Product Categories *",
            options=[c for c in IngredientCategory],
            format_func=lambda c: c.value.replace("_", " ").title(),
        )

        # Row 3: City, Country
        c1, c2 = st.columns(2)
        with c1:
            city = st.text_input("City *", value="Dubai")
        with c2:
            country = st.text_input("Country", value="UAE")

        # Row 4: Lead time, Min order
        c1, c2 = st.columns(2)
        with c1:
            lead_time = st.number_input("Lead Time (days)", min_value=0.5, value=1.0, step=0.5)
        with c2:
            min_order = st.number_input("Min Order Value (AED)", min_value=0.0, value=0.0, step=100.0)

        # Row 5: Reliability, Fill Rate
        c1, c2 = st.columns(2)
        with c1:
            reliability = st.slider("Reliability Score", 0.0, 1.0, 0.85, 0.01)
        with c2:
            fill_rate = st.slider("Fill Rate", 0.0, 1.0, 0.90, 0.01)

        # Row 6: Contact
        c1, c2 = st.columns(2)
        with c1:
            email = st.text_input("Contact Email *")
        with c2:
            phone = st.text_input("Contact Phone")

        is_active = st.checkbox("Active", value=True)

        submitted = st.form_submit_button("Register Supplier", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        # Validation
        if not name.strip():
            st.error("Supplier name is required.")
            return
        if not city.strip():
            st.error("City is required.")
            return
        if not categories:
            st.error("Select at least one product category.")
            return
        if not email.strip() or "@" not in email:
            st.error("A valid contact email is required.")
            return

        supplier = Supplier(
            name=name.strip(),
            tier=tier,
            categories=categories,
            city=city.strip(),
            country=country.strip() or "UAE",
            lead_time_days=lead_time,
            min_order_value=min_order,
            reliability_score=reliability,
            avg_fill_rate=fill_rate,
            contact_email=email.strip(),
            contact_phone=phone.strip(),
            is_active=is_active,
        )

        st.session_state.suppliers.append(supplier)
        network_count = len(st.session_state.suppliers)

        st.success(f"Supplier **{supplier.name}** registered successfully!")

        # Summary card
        cat_labels = ", ".join(c.value.replace("_", " ").title() for c in supplier.categories)
        st.markdown(
            f'<div class="section-card">'
            f'<div class="section-title">Registration Summary</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;">'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Name</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{supplier.name}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Tier</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{supplier.tier.value.title()}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Categories</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{cat_labels}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Location</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{supplier.city}, {supplier.country}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Lead Time</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{supplier.lead_time_days} days</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Reliability</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{supplier.reliability_score:.0%}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Contact</span><br>'
            f'<span style="font-weight:700;color:#2D3436;">{supplier.contact_email}</span></div>'
            f'<div><span style="color:#636e72;font-size:0.85rem;">Network Size</span><br>'
            f'<span style="font-weight:700;color:#FF6B35;">{network_count} suppliers</span></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
