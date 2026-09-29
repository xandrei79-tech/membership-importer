from datetime import date
from decimal import Decimal

import pytest

from membership_importer.allocation.rules.start_month_rule import StartMonthRule
from membership_importer.models.payment import Payment
from membership_importer.models.start_position import StartPosition


def _payment(payment_date: date) -> Payment:
    return Payment(
        payment_date=payment_date,
        amount=Decimal("10.00"),
        payer_name="Example Payer",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )


@pytest.mark.parametrize(
    ("payment_date", "expected_index", "expected_name"),
    [
        (date(2026, 3, 8), 2, "March"),
        (date(2026, 9, 17), 8, "September"),
        (date(2026, 12, 31), 11, "December"),
    ],
)
def test_start_month_rule_uses_payment_year_and_month(
    payment_date: date,
    expected_index: int,
    expected_name: str,
) -> None:
    payment = _payment(payment_date)

    result = StartMonthRule().determine(payment)

    assert result == StartPosition(
        year=2026,
        month_index=expected_index,
        month_name=expected_name,
    )
    assert payment.payment_date == payment_date
