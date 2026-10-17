"""How many returns, and courier pickups, to expect each day for the next four weeks (CX-152).

Pablo sends it to Fabrikam Logistics on Mondays, so they know how many vans to plan for while pickups are confirmed by
hand. It's deliberately simple: each weekday's average over the last eight weeks of returns_clean. Pickups are a share
of those returns, on the next day the courier collects.

It knows nothing about Trailhead 3. Once it goes on sale on November 3, add its returns by hand until there are eight
weeks of them.

    export FABRIC_SQL_ENDPOINT=...   # contoso_sales › SQL analytics endpoint › Copy SQL connection string
    python returns_forecast.py       # or --weeks 6

It needs Viewer on the workspace.
"""

import argparse
import datetime as dt
import os
import struct
from collections import defaultdict

import pyodbc
from azure.identity import DefaultAzureCredential

SQL_COPT_SS_ACCESS_TOKEN = 1256  # the ODBC driver's connection attribute for an Entra ID access token
WEEKS_BACK = 8

# Ana's guess from the support desk: about four customers in ten would rather not take a return anywhere. Replace it
# with the real share once there are four weeks of pickups (pickup_slots_capacity.sql).
PICKUP_SHARE = 0.4

# The courier doesn't collect on Sundays or national holidays. These are the holidays on weekdays until January.
NO_PICKUPS = {dt.date(2026, 12, 8), dt.date(2026, 12, 25), dt.date(2027, 1, 1), dt.date(2027, 1, 6)}

DAILY_RETURNS = """
SELECT opened_on, COUNT(*) AS returns
FROM dbo.returns_clean
WHERE opened_on >= DATEADD(week, -?, CAST(GETDATE() AS date)) AND opened_on < CAST(GETDATE() AS date)
GROUP BY opened_on
"""


def connect() -> pyodbc.Connection:
    """The SQL analytics endpoint of the contoso_sales lakehouse, signed in as you."""
    token = DefaultAzureCredential().get_token("https://database.windows.net/.default").token.encode("utf-16-le")
    return pyodbc.connect(
        f"Driver={{ODBC Driver 18 for SQL Server}};Server={os.environ['FABRIC_SQL_ENDPOINT']},1433;"
        "Database=contoso_sales;Encrypt=yes",
        attrs_before={SQL_COPT_SS_ACCESS_TOKEN: struct.pack(f"<I{len(token)}s", len(token), token)},
    )


def weekday_averages(rows: list[tuple[dt.date, int]]) -> list[float]:
    """Monday to Sunday, the returns opened on that weekday, on average. A day with none counts as zero."""
    totals = [0] * 7
    for opened_on, returns in rows:
        totals[opened_on.weekday()] += returns
    return [total / WEEKS_BACK for total in totals]


def pickup_day(day: dt.date) -> dt.date:
    """The first day after this one when the courier collects."""
    day += dt.timedelta(days=1)
    while day.weekday() == 6 or day in NO_PICKUPS:
        day += dt.timedelta(days=1)
    return day


def forecast(averages: list[float], start: dt.date, days: int) -> list[tuple[dt.date, float, float]]:
    """(day, returns, pickups) for each day from start."""
    returns = {day: averages[day.weekday()] for day in (start + dt.timedelta(days=n) for n in range(days))}
    pickups: defaultdict[dt.date, float] = defaultdict(float)
    for day, expected in returns.items():
        pickups[pickup_day(day)] += expected * PICKUP_SHARE
    return [(day, expected, pickups[day]) for day, expected in returns.items()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Returns and courier pickups to expect each day.")
    parser.add_argument("--weeks", type=int, default=4, help="how far ahead (default: 4)")
    args = parser.parse_args()
    with connect() as connection:
        rows = connection.cursor().execute(DAILY_RETURNS, WEEKS_BACK).fetchall()
    print(f"{'Day':<16}{'Returns':>8}{'Pickups':>9}")
    for day, returns, pickups in forecast(weekday_averages(rows), dt.date.today(), args.weeks * 7):
        print(f"{day:%a %d %b %Y}{returns:>8.0f}{pickups:>9.0f}")


if __name__ == "__main__":
    main()
