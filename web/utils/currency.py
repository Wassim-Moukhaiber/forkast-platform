"""
Multi-currency support for Forkast Platform
Supports AED, USD, and KWD with live-style conversion rates
"""
import streamlit as st

# Conversion rates from AED (base currency of demo data)
CURRENCIES = {
    "AED": {"symbol": "AED", "rate": 1.0, "name": "UAE Dirham", "flag": "🇦🇪", "decimal": 0},
    "USD": {"symbol": "$", "rate": 0.2723, "name": "US Dollar", "flag": "🇺🇸", "decimal": 2},
    "KWD": {"symbol": "KWD", "rate": 0.0838, "name": "Kuwaiti Dinar", "flag": "🇰🇼", "decimal": 3},
}


def get_currency():
    """Get the currently selected currency code"""
    return st.session_state.get("currency", "AED")


def get_currency_info():
    """Get full currency info dict for current selection"""
    return CURRENCIES[get_currency()]


def convert(amount_aed):
    """Convert an AED amount to the selected currency"""
    info = get_currency_info()
    return amount_aed * info["rate"]


def fmt(amount_aed, show_symbol=True, compact=False):
    """
    Format an AED amount in the selected currency.
    amount_aed: the value in AED (base currency of all demo data)
    show_symbol: whether to prefix with currency symbol
    compact: use K/M suffixes for large numbers
    """
    info = get_currency_info()
    converted = amount_aed * info["rate"]
    sym = info["symbol"]
    dec = info["decimal"]

    if compact and abs(converted) >= 1_000_000:
        formatted = f"{converted/1_000_000:,.{min(dec, 1)}f}M"
    elif compact and abs(converted) >= 10_000:
        formatted = f"{converted/1_000:,.{min(dec, 1)}f}K"
    else:
        formatted = f"{converted:,.{dec}f}"

    if show_symbol:
        return f"{sym} {formatted}" if sym != "$" else f"${formatted}"
    return formatted


def fmt_rate(amount_aed, suffix="", show_symbol=True):
    """Format a rate or per-unit value (e.g., cost per hour, cost per kg)"""
    info = get_currency_info()
    converted = amount_aed * info["rate"]
    sym = info["symbol"]
    dec = info["decimal"]
    formatted = f"{converted:,.{dec}f}"

    if show_symbol:
        prefix = f"{sym} " if sym != "$" else "$"
        return f"{prefix}{formatted}{suffix}"
    return f"{formatted}{suffix}"


def currency_label():
    """Return a display label like 'AED' or 'USD' for chart titles"""
    return get_currency_info()["symbol"]
