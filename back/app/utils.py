from calendar import monthrange
from datetime import date
from decimal import ROUND_HALF_UP, Decimal


def month_end(value: date) -> date:
    return value.replace(day=monthrange(value.year, value.month)[1])


def generate_schedule(
    amount: Decimal,
    nr_months: int,
    start_month: date,
) -> list[tuple[date, Decimal]]:
    """Full debt in month 0; no final zero row.

    Round the cumulative deduction, not an already-rounded monthly instalment.
    Example 100 / 3: 100.00, 66.67, 33.33.
    """
    if not amount.is_finite() or amount <= 0 or nr_months <= 0 or start_month.day != 1:
        raise ValueError("Invalid credit terms")
    exponent = amount.as_tuple().exponent
    if isinstance(exponent, int) and exponent < -2:
        raise ValueError("Amount must have at most two decimal places")
    if amount < Decimal("0.01") * nr_months:
        raise ValueError("Credit must allow at least 0.01 per month")
    first_index = (start_month.year - 1) * 12 + start_month.month - 1
    if first_index + nr_months > 9999 * 12:
        raise ValueError("Schedule exceeds the supported date range")
    rows = []
    for index in range(nr_months):
        year_index, month_index = divmod(first_index + index, 12)
        end = month_end(date(year_index + 1, month_index + 1, 1))
        deduction = (amount * index / nr_months).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        rows.append((end, amount - deduction))
    return rows
