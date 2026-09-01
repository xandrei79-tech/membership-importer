from datetime import date
from decimal import Decimal

from membership_importer.models.member import Member
from membership_importer.models.payment import Payment


def make_payment(amount: str) -> Payment:
    return Payment(
        payment_date=date(2026, 8, 27),
        amount=Decimal(amount),
        payer_name="Member",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )


def test_member_defaults_have_no_payments() -> None:
    member = Member(mac="MAC-001", full_name="Test Member")

    assert member.active is True
    assert member.notes == ""
    assert member.payments == []
    assert member.total_paid() == Decimal("0")
    assert member.has_payments() is False


def test_member_adds_payments_and_calculates_total() -> None:
    member = Member(mac="MAC-001", full_name="Test Member")
    first_payment = make_payment("10.00")
    second_payment = make_payment("7.50")

    member.add_payment(first_payment)
    member.add_payment(second_payment)

    assert member.payments == [first_payment, second_payment]
    assert member.total_paid() == Decimal("17.50")
    assert member.has_payments() is True


def test_members_do_not_share_payment_lists() -> None:
    first_member = Member(mac="MAC-001", full_name="First Member")
    second_member = Member(mac="MAC-002", full_name="Second Member")

    first_member.add_payment(make_payment("10.00"))

    assert first_member.has_payments() is True
    assert second_member.has_payments() is False