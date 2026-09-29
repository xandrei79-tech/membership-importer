"""Orchestrate allocation planning rules."""

from decimal import Decimal

from ..models.allocation_plan import AllocationPlan
from ..models.customer import Customer
from ..models.payment import Payment
from .calendar import Calendar


class AllocationEngine:
    """Allocate full monthly fees without crossing a worksheet year boundary."""

    def __init__(
        self,
        calendar: Calendar | None = None,
    ) -> None:
        self._calendar = calendar if calendar is not None else Calendar()

    def allocate(self, payment: Payment, customer: Customer) -> AllocationPlan:
        """Return a plan allocating as many full monthly fees as the payment covers."""
        if customer.group is None or customer.group.monthly_amount <= Decimal("0"):
            raise ValueError("Customer must have a payment group with a positive monthly fee.")
        if len(customer.members) != 1:
            raise ValueError("Allocation currently requires exactly one customer member.")

        monthly_fee = customer.group.monthly_amount
        member = customer.members[0]
        position = self._calendar.first(payment.payment_date)
        amount_remaining = payment.amount
        amount_allocated = Decimal("0")
        allocations: list[object] = []

        while amount_remaining >= monthly_fee:
            period = f"{position.year}-{position.month_index + 1:02d}"
            if member.month_availability.is_available(position):
                allocations.append({"period": period, "amount": monthly_fee})
                amount_remaining -= monthly_fee
                amount_allocated += monthly_fee

            position = self._calendar.next(position)

        return AllocationPlan(
            customer=customer,
            payment=payment,
            allocations=allocations,
            amount_allocated=amount_allocated,
            amount_remaining=amount_remaining,
            warnings=[],
            status="planned",
        )
