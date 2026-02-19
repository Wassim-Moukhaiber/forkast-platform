"""Procurement Page - Enhanced"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from inventory.optimizer import InventoryOptimizer
from web.utils.currency import fmt, fmt_rate, currency_label, convert
from web.assets.images import render_svg, PROCUREMENT_HEADER_SVG


def show():
    st.markdown('<p class="main-header">Smart Procurement</p>', unsafe_allow_html=True)
    st.markdown(render_svg(PROCUREMENT_HEADER_SVG, width="100%"), unsafe_allow_html=True)
    st.markdown('<p class="page-desc">AI-generated procurement drafts with human-in-the-loop approval.</p>', unsafe_allow_html=True)

    optimizer = InventoryOptimizer()
    inventory = st.session_state.inventory
    suppliers = st.session_state.suppliers

    tab1, tab2 = st.tabs(["📝 Reorder Recommendations", "📄 Procurement Drafts"])

    with tab1:
        st.markdown('<div class="section-title">AI Reorder Recommendations</div>', unsafe_allow_html=True)
        days = st.slider("Plan for days ahead:", 3, 14, 7, key="proc_days")
        recs = optimizer.generate_reorder_recommendations(inventory, days_ahead=days)

        if not recs:
            st.markdown(
                '<div class="alert-low"><strong>All Clear</strong><br>'
                'All inventory levels are healthy. No reorders needed.</div>',
                unsafe_allow_html=True
            )
            return

        # Summary KPIs
        total_cost = sum(r['estimated_cost'] for r in recs)
        critical = sum(1 for r in recs if r['priority'] == 'critical')
        high = sum(1 for r in recs if r['priority'] == 'high')

        col1, col2, col3, col4 = st.columns(4)
        kpis = [
            ("kpi-icon-green", "💰", fmt(total_cost), "TOTAL EST. COST"),
            ("kpi-icon-red", "🚨", str(critical), "CRITICAL ITEMS"),
            ("kpi-icon-orange", "⚠️", str(high), "HIGH PRIORITY"),
            ("kpi-icon-blue", "📦", str(len(recs)), "TOTAL ITEMS"),
        ]
        for col, (icon_cls, emoji, val, lbl) in zip([col1, col2, col3, col4], kpis):
            with col:
                st.markdown(f'''<div class="kpi-card">
                    <div class="kpi-icon {icon_cls}">{emoji}</div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-label">{lbl}</div>
                </div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Recommendations list
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        for rec in recs:
            priority = rec['priority']
            css_class = f"alert-{priority}" if priority in ('critical', 'high', 'medium', 'low') else "alert-medium"
            badge_class = f"badge-{priority}" if priority in ('critical', 'high', 'medium', 'low') else "badge-medium"
            st.markdown(
                f'<div class="{css_class}" style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div>'
                f'<strong>{rec["item_name"]}</strong> <span class="badge {badge_class}">{priority.upper()}</span>'
                f'<br><span style="font-size:0.85rem;color:#636e72;">{rec["category"]} | '
                f'Current: {rec["current_stock"]} {rec["unit"]} | Days left: {rec["days_remaining"]:.0f}</span>'
                f'</div>'
                f'<div style="text-align:right;">'
                f'<div style="font-weight:700;font-size:1.1rem;">Order: {rec["order_quantity"]} {rec["unit"]}</div>'
                f'<div style="color:#636e72;font-size:0.85rem;">{fmt(rec["estimated_cost"])}</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.reorder_recs = recs

    with tab2:
        st.markdown('<div class="section-title">Auto-Generated Procurement Drafts</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="alert-medium">'
            '<strong>Human-in-the-Loop</strong><br>'
            'These drafts are AI-generated recommendations. Review and approve before sending to suppliers.'
            '</div>',
            unsafe_allow_html=True
        )

        if 'reorder_recs' not in st.session_state:
            st.warning("Generate reorder recommendations first.")
            return

        recs = st.session_state.reorder_recs
        drafts = optimizer.generate_procurement_draft(recs, suppliers)

        if not drafts:
            st.info("No procurement drafts to generate.")
            return

        for i, order in enumerate(drafts):
            supplier = next((s for s in suppliers if s.uid == order.supplier_uid), None)
            supplier_name = supplier.name if supplier else order.supplier_uid

            with st.expander(f"PO Draft #{i+1} - {supplier_name} | {fmt(order.total_value, show_symbol=False)}", expanded=(i==0)):
                st.markdown('<div class="section-card">', unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'''<div style="padding:0.3rem 0;">
                        <div style="font-size:0.75rem;color:#636e72;text-transform:uppercase;">Supplier</div>
                        <div style="font-weight:700;font-size:1rem;">{supplier_name}</div>
                    </div>''', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'''<div style="padding:0.3rem 0;">
                        <div style="font-size:0.75rem;color:#636e72;text-transform:uppercase;">Delivery Date</div>
                        <div style="font-weight:700;font-size:1rem;">{order.expected_delivery.strftime('%Y-%m-%d')}</div>
                    </div>''', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'''<div style="padding:0.3rem 0;">
                        <div style="font-size:0.75rem;color:#636e72;text-transform:uppercase;">Total Value</div>
                        <div style="font-weight:700;font-size:1rem;color:#FF6B35;">{fmt(order.total_value)}</div>
                    </div>''', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                items_table = []
                for item in order.items:
                    items_table.append({
                        "Item": item['item_name'],
                        "Qty": f"{item['quantity']} {item['unit']}",
                        "Unit Cost": fmt_rate(item['unit_cost']),
                        "Total": fmt(item['total'])
                    })
                st.dataframe(items_table, use_container_width=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"Approve & Send", key=f"approve_{i}"):
                        st.success(f"PO sent to {supplier_name}!")
                with col2:
                    if st.button(f"Edit Draft", key=f"edit_{i}"):
                        st.info("Edit mode - adjust quantities as needed")
                with col3:
                    if st.button(f"Reject", key=f"reject_{i}"):
                        st.warning("Draft rejected")

                st.markdown('</div>', unsafe_allow_html=True)
