from datetime import date
from decimal import Decimal
from pathlib import Path

from membership_importer.models.import_result import ImportResult
from membership_importer.models.payment import Payment
from membership_importer.models.workbook import Workbook


def make_payment(amount: str) -> Payment:
    return Payment(
        payment_date=date(2026, 8, 27),
        amount=Decimal(amount),
        payer_name="Test Member",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )


def test_import_result_collects_payments() -> None:
    result = ImportResult(workbook=Workbook(path=Path("membership.xlsx")))
    first_payment = make_payment("10.00")
    second_payment = make_payment("7.50")

    assert result.has_payments() is False
    result.add_payment(first_payment)
    result.add_payment(second_payment)

    assert result.payments == [first_payment, second_payment]
    assert result.total_paid() == Decimal("17.50")
    assert result.has_payments() is True
