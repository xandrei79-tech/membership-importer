"""Determine the starting worksheet year and month for a payment."""

from ...models.payment import Payment
from ...models.start_position import StartPosition


class StartMonthRule:
    """Select the payment's calendar year and month as its start position."""

    MONTH_NAMES = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )

    def determine(self, payment: Payment) -> StartPosition:
        """Return the year and month corresponding to ``payment.payment_date``."""
        payment_date = payment.payment_date
        month_index = payment_date.month - 1
        return StartPosition(
            year=payment_date.year,
            month_index=month_index,
            month_name=self.MONTH_NAMES[month_index],
        )