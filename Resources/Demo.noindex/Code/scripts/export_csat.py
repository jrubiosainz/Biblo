# /// script
# requires-python = ">=3.10"
# dependencies = ["deltalake", "pyarrow", "azure-identity"]
# ///
"""Copies the returns assistant pilot's week-by-week numbers from OneLake to a CSV, for slides.

Ana's weekly report reads `csat_weekly` from OneLake by itself, but PowerPoint can't: the *CSAT by week* chart in
Lucía's Data Summit keynote is made from this script's CSV. `csat_by_week.ipynb` rewrites the table on Thursdays at
16:00, so run this after that.

    export FABRIC_WORKSPACE_ID=...    # Contoso Sales: it's in the workspace's URL
    export FABRIC_LAKEHOUSE_ID=...    # contoso_sales: it's in the lakehouse's URL
    az login
    uv run export_csat.py

It reads the Delta table straight from OneLake with your own sign-in: no Spark, no capacity, and Viewer on the
workspace is enough. On Thursday, October 15, it printed:

    week        conversations  resolved  ratings  csat
    2026-09-14            642       41%      205   4.1
    2026-09-21            871       49%      283   4.2
    2026-09-28          1,043       55%      344   4.3
    2026-10-05          1,398       62%      468   4.5
    2026-10-12          1,186       67%      401   4.6  so far

    Target 4.5: met in the week of October 12. Wrote csat_weekly.csv.

Javier Molina, October 15, 2026.
"""

from __future__ import annotations

import csv
import os
import sys
from datetime import date, timedelta
from pathlib import Path

TARGET = 4.5
TOO_FEW = 100  # fewer ratings than this and a tenth means nothing: the notebook's rule
COLUMNS = ["week", "conversations", "resolved_pct", "ratings", "csat"]
OUT = Path("csat_weekly.csv")


def read_weeks() -> list[dict]:
    from azure.identity import DefaultAzureCredential
    from deltalake import DeltaTable

    workspace, lakehouse = os.environ["FABRIC_WORKSPACE_ID"], os.environ["FABRIC_LAKEHOUSE_ID"]
    # OneLake speaks the Azure Storage API, so it takes a storage token.
    token = DefaultAzureCredential().get_token("https://storage.azure.com/.default").token
    table = DeltaTable(
        f"abfss://{workspace}@onelake.dfs.fabric.microsoft.com/{lakehouse}/Tables/csat_weekly",
        storage_options={"bearer_token": token, "use_fabric_endpoint": "true"},
    )
    return sorted(table.to_pyarrow_table(columns=COLUMNS).to_pylist(), key=lambda row: row["week"])


def report(weeks: list[dict], today: date) -> list[str]:
    lines = [f"{'week':<10}  {'conversations':>13}  {'resolved':>8}  {'ratings':>7}  {'csat':>4}"]
    for row in weeks:
        if row["ratings"] < TOO_FEW:
            note = "  too few ratings to read"
        elif row["week"] + timedelta(days=7) > today:
            note = "  so far"
        else:
            note = ""
        lines.append(f"{row['week']:%Y-%m-%d}  {row['conversations']:>13,}  {row['resolved_pct']:>7}%  "
                     f"{row['ratings']:>7}  {row['csat']:>4.1f}{note}")
    latest = weeks[-1]
    verdict = "met" if latest["csat"] >= TARGET else "not met"
    lines += ["", f"Target {TARGET}: {verdict} in the week of {latest['week']:%B} {latest['week'].day}. Wrote {OUT}."]
    return lines


def main() -> None:
    weeks = read_weeks()
    if not weeks:
        sys.exit("csat_weekly is empty: has csat_by_week.ipynb run since the pilot started?")
    with OUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows({**row, "week": row["week"].isoformat()} for row in weeks)
    print("\n".join(report(weeks, date.today())))


if __name__ == "__main__":
    main()
