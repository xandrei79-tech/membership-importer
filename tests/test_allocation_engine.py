from datetime import date
from decimal import Decimal

import pytest

from membership_importer.allocation.allocation_engine import AllocationEngine
from membership_importer.allocation.calendar import Calendar
from membership_importer.models.allocation_plan import AllocationPlan
from membership_importer.models.customer import Customer
from membership_importer.models.member import Member
from membership_importer.models.month_availability import MonthState
from membership_importer.models.payment import Payment
from membership_importer.models.payment_group import PaymentGroup


def _payment(amount: str) -> Payment:
    return Payment(
        payment_date=date(2026, 3, 1),
        amount=Decimal(amount),
        payer_name="Example Payer",
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record=None,
    )


def test_allocation_engine_can_be_constructed_with_default_calendar() -> None:
    engine = AllocationEngine()

    assert isinstance(engine._calendar, Calendar)


def test_allocation_engine_accepts_injected_calendar() -> None:
    calendar = Calendar()

    engine = AllocationEngine(calendar=calendar)

    assert engine._calendar is calendar


@pytest.mark.parametrize(
    ("payment_amount", "expected_periods", "expected_allocated", "expected_remaining"),
    [
        ("36.00", ["2026-03", "2026-04", "2026-05"], "36.00", "0.00"),
        ("24.00", ["2026-03", "2026-04"], "24.00", "0.00"),
        ("12.00", ["2026-03"], "12.00", "0.00"),
        ("6.00", [], "0.00", "6.00"),
    ],
)
def test_allocate_assigns_full_months_from_payment_month(
    payment_amount: str,
    expected_periods: list[str],
    expected_allocated: str,
    expected_remaining: str,
) -> None:
    payment = _payment(payment_amount)
    customer = Customer(
        customer_id="CUST-01",
        customer_name="Example Customer",
        group=PaymentGroup(name="Standard", monthly_amount=Decimal("12.00")),
        members=[Member(mac="AA:BB:CC:DD:EE:FF", full_name="Example Member")],
    )

    plan = AllocationEngine().allocate(payment, customer)

    assert isinstance(plan, AllocationPlan)
    assert plan.payment is payment
    assert plan.customer is customer
    assert [allocation["period"] for allocation in plan.allocations] == expected_periods
    assert all(
        allocation["amount"] == Decimal("12.00")
        for allocation in plan.allocations
    )
    assert plan.amount_allocated == Decimal(expected_allocated)
    assert plan.amount_remaining == Decimal(expected_remaining)
    assert plan.warnings == []
    assert plan.status == "planned"


def test_allocate_skips_already_paid_month_and_continues_forward() -> None:
    payment = _payment("36.00")
    member = Member(
        mac="AA:BB:CC:DD:EE:FF",
        full_name="Example Member",
    )
    member.month_availability.set_state(Calendar().first(payment.payment_date), MonthState.PAID)
    customer = Customer(
        customer_id="CUST-01",
        customer_name="Example Customer",
        group=PaymentGroup(name="Standard", monthly_amount=Decimal("12.00")),
        members=[member],
    )

    plan = AllocationEngine().allocate(payment, customer)

    assert [allocation["period"] for allocation in plan.allocations] == [
        "2026-04",
        "2026-05",
        "2026-06",
    ]
    assert plan.amount_allocated == Decimal("36.00")
    assert plan.amount_remaining == Decimal("0.00")
