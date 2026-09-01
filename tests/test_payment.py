from datetime import date
from decimal import Decimal

from membership_importer.models.payment import Payment


def test_payment_helpers() -> None:
    payment = Payment(
        payment_date=date(2026, 8, 27),
        amount=Decimal("10.00"),
        payer_name="Test Member",
        description="Membership fee",
        reference_number="REF-001",
        source_bank="Test bank",
        original_record={"amount": "10.00"},
    )

    assert payment.has_reference_number() is True
    assert payment.is_from_bank("Test bank") is True
    assert payment.is_from_bank("Other bank") is False


def test_payment_without_reference_number() -> None:
    payment = Payment(
        payment_date=date(2026, 8, 27),
        amount=Decimal("10.00"),
        payer_name="Test Member",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )

    assert payment.has_reference_number() is False
