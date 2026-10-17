"""Name badges for Data Summit Madrid 2026, and the menu counts for Fourth Coffee.

Reads the registration site's export and writes badges.html: eight badges to an A4 page, two across and four down,
105 × 74 mm each, the size of the perforated badge sheets. Print it at 100 %, not "fit to page", and the perforations
line up. Badges are sorted by last name, the order they're laid out on the registration desks.

    python3 summit_badges.py registrations.csv            # writes badges.html
    python3 summit_badges.py registrations.csv out.html

The first name is the biggest thing on the badge: it's what people read from across a coffee table. A strip at the
bottom says Speaker, Staff or Attendee, in a color you can tell apart from across the room.

Menus aren't printed on badges: what someone can't eat can say something about their health. Fourth Coffee only gets
the counts, which this prints, and serves the special menus from its own counter at lunch. The summit is on Thursday,
November 12: doors at 8:00, coffee at 10:30 and 16:00, standing lunch at 14:00. It printed, for example:

    900 registered: 852 attendees, 22 speakers, 26 staff.
    Menus for Fourth Coffee: 801 standard, 59 vegetarian, 40 gluten-free.
    Wrote badges.html: 113 A4 pages.

Needs nothing but Python 3.9 or later.
"""

from __future__ import annotations

import csv
import html
import math
import sys
import unicodedata
from collections import Counter
from pathlib import Path

PER_PAGE = 8
ROLES = {"Attendee": "attendee", "Speaker": "speaker", "Staff": "staff"}
MENUS = {"": "standard", "None": "standard", "Vegetarian": "vegetarian", "Gluten-free": "gluten-free"}

CSS = """@page { size: A4; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; font-family: "Helvetica Neue", Arial, sans-serif; color: #050510 }
.sheet { display: grid; grid-template-columns: repeat(2, 105mm); grid-template-rows: repeat(4, 74.25mm);
  width: 210mm; height: 297mm; break-after: page }
.badge { position: relative; overflow: hidden; padding: 8mm 9mm 0; outline: 0.2mm dashed #d4d4d8 }
.event { font-size: 7pt; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: #52525b }
.first { margin-top: 6mm; font-size: 32pt; font-weight: 800; line-height: 1; letter-spacing: -0.02em;
  white-space: nowrap }
.first.long { font-size: 25pt }
.first.longer { font-size: 19pt }
.who { margin-top: 2.5mm; font-size: 10pt; color: #3f3f46 }
.role { position: absolute; left: 0; right: 0; bottom: 0; height: 12mm; padding: 0 9mm; display: flex;
  align-items: center; font-size: 9pt; font-weight: 800; letter-spacing: 0.24em; text-transform: uppercase;
  color: #fff; background: #050510 }
.speaker .role { background: #6d28d9 }
.staff .role { color: #050510; background: #22d3ee }
"""


def sort_key(person: dict) -> tuple[str, str]:
    """Last name, then first name, ignoring accents and case: Álvarez goes with the A's."""
    def plain(text: str) -> str:
        decomposed = unicodedata.normalize("NFKD", text)
        return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()
    return plain(person["Last name"]), plain(person["First name"])


def badge(person: dict) -> str:
    first, role = person["First name"], person["Ticket"]
    size = "" if len(first) <= 9 else " long" if len(first) <= 12 else " longer"
    who = " · ".join(html.escape(part) for part in (f"{first} {person['Last name']}", person["Company"]) if part)
    return (f'<div class="badge {ROLES[role]}"><div class="event">Data Summit Madrid · 12 nov 2026</div>'
            f'<div class="first{size}">{html.escape(first)}</div><div class="who">{who}</div>'
            f'<div class="role">{role}</div></div>')


def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: summit_badges.py registrations.csv [badges.html]")
    source = Path(sys.argv[1])
    target = Path(sys.argv[2] if len(sys.argv) == 3 else "badges.html")

    # The registration site exports UTF-8 with a byte order mark, for Excel.
    with source.open(newline="", encoding="utf-8-sig") as file:
        people = sorted(({key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(file)),
                        key=sort_key)
    unknown = {person["Ticket"] for person in people} - ROLES.keys()
    unknown |= {person["Menu"] for person in people} - MENUS.keys()
    if unknown:
        sys.exit(f"unexpected values in the export: {', '.join(sorted(unknown))}")

    pages = [people[start:start + PER_PAGE] for start in range(0, len(people), PER_PAGE)]
    sheets = "\n".join('<section class="sheet">' + "".join(badge(person) for person in page) + "</section>"
                       for page in pages)
    target.write_text(f'<!doctype html>\n<html lang="es"><meta charset="utf-8"><title>Data Summit Madrid · '
                      f'badges</title>\n<style>\n{CSS}</style>\n{sheets}\n</html>\n', encoding="utf-8")

    roles = Counter(ROLES[person["Ticket"]] for person in people)
    menus = Counter(MENUS[person["Menu"]] for person in people)
    print(f"{len(people)} registered: {roles['attendee']} attendees, {roles['speaker']} speakers, "
          f"{roles['staff']} staff.")
    print(f"Menus for Fourth Coffee: {menus['standard']} standard, {menus['vegetarian']} vegetarian, "
          f"{menus['gluten-free']} gluten-free.")
    print(f"Wrote {target}: {math.ceil(len(people) / PER_PAGE)} A4 pages.")


if __name__ == "__main__":
    main()
