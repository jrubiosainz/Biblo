"""When the courier can collect a return, and what it costs the customer (CX-138).

Fabrikam Logistics collects Monday to Saturday, in six 2-hour slots from 8:00 to 20:00, except on national holidays.
A slot can be booked until 20:00 the day before, Madrid time, and up to two weeks ahead. Collection is free when the
item arrived damaged, was the wrong item or isn't as described; when the customer just doesn't need it any more, it
costs €4.95.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from zoneinfo import ZoneInfo

MADRID = ZoneInfo("Europe/Madrid")
SLOTS = ("08:00–10:00", "10:00–12:00", "12:00–14:00", "14:00–16:00", "16:00–18:00", "18:00–20:00")
CUTOFF = dt.time(20, 0)  # the day before
DAYS_AHEAD = 14

# From the BOE's calendar. Regional and local holidays don't stop the courier.
HOLIDAYS = {
    dt.date(2026, 10, 12), dt.date(2026, 11, 1), dt.date(2026, 12, 6), dt.date(2026, 12, 8), dt.date(2026, 12, 25),
    dt.date(2027, 1, 1), dt.date(2027, 1, 6), dt.date(2027, 3, 26), dt.date(2027, 5, 1), dt.date(2027, 8, 15),
    dt.date(2027, 10, 12), dt.date(2027, 11, 1), dt.date(2027, 12, 6), dt.date(2027, 12, 8), dt.date(2027, 12, 25),
}

FREE_REASONS = {"damaged", "wrong_item", "not_as_described"}  # our fault, so our courier
FEE = Decimal("4.95")


def fee(reason: str) -> Decimal:
    """What the customer pays for the courier: nothing when it's our fault, €4.95 when they changed their mind."""
    return Decimal(0) if reason in FREE_REASONS else FEE


def collects_on(day: dt.date) -> bool:
    """Monday to Saturday, except national holidays."""
    return day.weekday() < 6 and day not in HOLIDAYS


def bookable_days(now: dt.datetime | None = None) -> list[dt.date]:
    """The days a customer can still choose: from tomorrow, or the day after once it's past 20:00, for two weeks."""
    now = (now or dt.datetime.now(MADRID)).astimezone(MADRID)
    first = now.date() + dt.timedelta(days=1 if now.time() < CUTOFF else 2)
    return [day for day in (first + dt.timedelta(days=n) for n in range(DAYS_AHEAD)) if collects_on(day)]


def check(day: dt.date, slot: str, now: dt.datetime | None = None) -> None:
    """Refuses a pickup the courier can't do, in words the agent can pass on, with the next days that work."""
    if slot not in SLOTS:
        raise ValueError(f"Pickups go in 2-hour slots: {', '.join(SLOTS)}.")
    days = bookable_days(now)
    if day not in days:
        raise ValueError(f"The courier can't come on {day.isoformat()}. Pickups are Monday to Saturday, never on a "
                         "national holiday, and must be booked by 20:00 the day before. The next days are "
                         f"{', '.join(d.isoformat() for d in days[:3])}.")
