from datetime import date
from decimal import Decimal

from membership_importer.models.allocation_plan import AllocationPlan
from membership_importer.models.customer import Customer
from membership_importer.models.payment import Payment


def test_allocation_plan_stores_requested_domain_fields() -> None:
    customer = Customer(customer_id="CUST-01", customer_name="Alice Example")
    payment = Payment(
        payment_date=date(2025, 1, 15),
        amount=Decimal("25.00"),
        payer_name="Alice Example",
        description="Membership fee",
        reference_number="REF-01",
        source_bank="Test bank",
        original_record=None,
    )
    allocations = [{"period": "2025-01", "amount": Decimal("10.00")}]
    warnings = ["Remaining balance carried forward"]

    plan = AllocationPlan(
        customer=customer,
        payment=payment,
        allocations=allocations,
        amount_allocated=Decimal("10.00"),
        amount_remaining=Decimal("15.00"),
        warnings=warnings,
        status="planned",
    )

    assert plan.customer is customer
    assert plan.payment is payment
    assert plan.allocations is allocations
    assert plan.amount_allocated == Decimal("10.00")
    assert plan.amount_remaining == Decimal("15.00")
    assert plan.warnings is warnings
    assert plan.status == "planned"
    assert payment.amount == Decimal("25.00")
    assert customer.members == []
