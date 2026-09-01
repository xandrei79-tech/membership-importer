from datetime import date
from decimal import Decimal
from pathlib import Path

from membership_importer.models.import_session import ImportSession
from membership_importer.models.payment import Payment
from membership_importer.models.workbook import Workbook


def test_import_session_tracks_workbook_payments_and_completion() -> None:
    session = ImportSession()
    workbook = Workbook(path=Path("membership.xlsx"))
    payment = Payment(
        payment_date=date(2026, 8, 27),
        amount=Decimal("10.00"),
        payer_name="Test Member",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )

    assert session.workbook is None
    assert session.is_complete() is False
    session.set_workbook(workbook)
    session.add_payment(payment)
    session.complete()

    assert session.workbook is workbook
    assert session.payments == [payment]
    assert session.total_paid() == Decimal("10.00")
    assert session.is_complete() is True


def test_import_sessions_do_not_share_payments() -> None:
    first_session = ImportSession()
    second_session = ImportSession()
    payment = Payment(
        payment_date=date(2026, 8, 27),
        amount=Decimal("10.00"),
        payer_name="Test Member",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )

    first_session.add_payment(payment)

    assert first_session.payments == [payment]
    assert second_session.payments == []
