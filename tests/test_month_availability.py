from membership_importer.models.month_availability import MonthAvailability, MonthState
from membership_importer.models.start_position import StartPosition


def test_month_availability_defaults_unrecorded_months_to_empty() -> None:
    availability = MonthAvailability()
    march = StartPosition(year=2026, month_index=2, month_name="March")

    assert availability.state_for(march) is MonthState.EMPTY
    assert availability.is_available(march) is True


def test_month_availability_marks_paid_month_as_unavailable() -> None:
    availability = MonthAvailability()
    march = StartPosition(year=2026, month_index=2, month_name="March")
    availability.set_state(march, MonthState.PAID)

    assert availability.state_for(march) is MonthState.PAID
    assert availability.is_available(march) is False