"""
Forkast Stripe Service
Wraps Stripe SDK for checkout sessions, webhooks, and refunds
"""
import stripe
from typing import Optional, Dict, Any
from api.config import settings

stripe.api_key = settings.stripe_secret_key


class StripeService:
    """Stripe payment operations for Forkast."""

    @staticmethod
    def create_checkout_session(
        amount_aed: float,
        currency: str,
        description: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> stripe.checkout.Session:
        """Create a Stripe Checkout Session."""
        amount_minor = int(amount_aed * 100)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency.lower(),
                    "product_data": {"name": description or "Forkast Payment"},
                    "unit_amount": amount_minor,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            metadata=metadata or {},
        )
        return session

    @staticmethod
    def retrieve_session(session_id: str) -> stripe.checkout.Session:
        """Retrieve a Checkout Session by ID."""
        return stripe.checkout.Session.retrieve(session_id)

    @staticmethod
    def construct_webhook_event(payload: bytes, sig_header: str) -> stripe.Event:
        """Verify and construct a Stripe webhook event."""
        return stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )

    @staticmethod
    def create_refund(
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: str = "requested_by_customer",
    ) -> stripe.Refund:
        """Create a refund for a payment."""
        params: Dict[str, Any] = {
            "payment_intent": payment_intent_id,
            "reason": reason,
        }
        if amount is not None:
            params["amount"] = amount
        return stripe.Refund.create(**params)

    @staticmethod
    def is_configured() -> bool:
        """Check if Stripe keys are configured."""
        return bool(settings.stripe_secret_key)
