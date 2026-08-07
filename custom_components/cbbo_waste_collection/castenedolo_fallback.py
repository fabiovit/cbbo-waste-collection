"""Bundled Castenedolo 2026 collection calendar.

The base weekday pattern is taken from the official CBBO 2026 Ecocalendario.
Exceptional New Year shifts shown in the official calendar are included.
"""
from __future__ import annotations

from datetime import date, timedelta

from .schedule import (
    Collection,
    GLASS_CANS,
    LABELS,
    ORGANIC,
    PAPER,
    PLASTIC,
    RESIDUAL,
    SANITARY,
)

YEAR = 2026

# Monday organic; Tuesday plastic + glass/cans; Wednesday paper;
# Thursday organic; Friday residual + sanitary.
_WEEKLY: dict[int, tuple[str, ...]] = {
    0: (ORGANIC,),
    1: (PLASTIC, GLASS_CANS),
    2: (PAPER,),
    3: (ORGANIC,),
    4: (RESIDUAL, SANITARY),
}

# New Year variations visible in the official January 2026 calendar.
# 1 Jan (organic) moves to 2 Jan; 2 Jan (residual/sanitary) moves to 3 Jan.
_REMOVE = {date(2026, 1, 1)}
_OVERRIDES: dict[date, tuple[str, ...]] = {
    date(2026, 1, 2): (ORGANIC,),
    date(2026, 1, 3): (RESIDUAL, SANITARY),
}


def build() -> list[Collection]:
    """Build the bundled Castenedolo 2026 base collection calendar."""
    result: list[Collection] = []
    day = date(YEAR, 1, 1)
    end = date(YEAR, 12, 31)
    while day <= end:
        if day in _OVERRIDES:
            types = _OVERRIDES[day]
        elif day in _REMOVE:
            day += timedelta(days=1)
            continue
        else:
            types = _WEEKLY.get(day.weekday(), ())

        if types:
            result.append(Collection(day, types, tuple(LABELS[item] for item in types)))
        day += timedelta(days=1)
    return result
