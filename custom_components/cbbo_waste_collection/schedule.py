"""Calendar rules for CBBO waste collection in Mazzano."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from .const import ZONE_NORTH, ZONE_SOUTH

ORGANIC = "organic"
PLASTIC = "plastic"
PAPER = "paper"
GLASS_CANS = "glass_cans"
RESIDUAL = "residual"
SANITARY = "sanitary"
GREEN = "green"

LABELS = {
    ORGANIC: "Frazione organica",
    PLASTIC: "Imballaggi in plastica",
    PAPER: "Carta e cartone",
    GLASS_CANS: "Vetro e lattine",
    RESIDUAL: "Rifiuto non riciclabile",
    SANITARY: "Tessili sanitari",
    GREEN: "Verde",
}

ICONS = {
    ORGANIC: "mdi:food-apple",
    PLASTIC: "mdi:bottle-soda",
    PAPER: "mdi:package-variant",
    GLASS_CANS: "mdi:bottle-wine",
    RESIDUAL: "mdi:trash-can",
    SANITARY: "mdi:baby-face-outline",
    GREEN: "mdi:leaf",
}

@dataclass(frozen=True, slots=True)
class Collection:
    day: date
    waste_types: tuple[str, ...]


def _residual_zone(day: date) -> str:
    """Return the zone served on a Wednesday.

    The 2026 calendar alternates North/South every Wednesday. The reference
    week shown by CBBO has South on 2026-07-01 and North on 2026-07-08.
    """
    anchor = date(2026, 7, 1)
    weeks = (day - anchor).days // 7
    return ZONE_SOUTH if weeks % 2 == 0 else ZONE_NORTH


def collections_for_day(
    day: date,
    zone: str,
    include_green: bool = True,
    include_sanitary: bool = True,
) -> tuple[str, ...]:
    """Return collections for a date.

    Rules are taken from the official 2026 Mazzano ecocalendar. The annual
    layout is recurring by weekday, with green seasonal frequency and an
    additional Saturday organic collection in summer.
    """
    if day.year not in (2026, 2027):
        return ()

    result: list[str] = []
    weekday = day.weekday()  # Mon=0

    if weekday in (0, 3):
        result.append(ORGANIC)

    if weekday == 1:
        result.append(PLASTIC)
        if include_green:
            # Weekly March-October; fortnightly January-February and November-December.
            if 3 <= day.month <= 10:
                result.append(GREEN)
            elif day.isocalendar().week % 2 == 0:
                result.append(GREEN)

    if weekday == 2:
        result.append(GLASS_CANS)
        if include_sanitary:
            result.append(SANITARY)
        if _residual_zone(day) == zone:
            result.append(RESIDUAL)

    if weekday == 4:
        result.append(PAPER)

    if weekday == 5 and include_sanitary:
        result.append(SANITARY)

    # Additional organic collection shown from June through August.
    if weekday == 5 and 6 <= day.month <= 8:
        result.insert(0, ORGANIC)

    return tuple(result)


def next_collection(
    start: date,
    zone: str,
    include_green: bool = True,
    include_sanitary: bool = True,
    *,
    include_start: bool = True,
    max_days: int = 370,
) -> Collection | None:
    """Find the next collection day."""
    offset = 0 if include_start else 1
    for days in range(offset, max_days + 1):
        candidate = start + timedelta(days=days)
        waste = collections_for_day(candidate, zone, include_green, include_sanitary)
        if waste:
            return Collection(candidate, waste)
    return None


def upcoming_collections(
    start: date,
    zone: str,
    include_green: bool = True,
    include_sanitary: bool = True,
    days: int = 14,
) -> Iterable[Collection]:
    """Yield collection days in a range."""
    for offset in range(days + 1):
        candidate = start + timedelta(days=offset)
        waste = collections_for_day(candidate, zone, include_green, include_sanitary)
        if waste:
            yield Collection(candidate, waste)
