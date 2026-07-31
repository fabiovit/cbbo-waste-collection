"""Conservative 2026 fallback for Mazzano when the CBBO page is unavailable."""
from __future__ import annotations
from datetime import date, timedelta
from .const import ZONE_NORTH, ZONE_SOUTH
from .schedule import Collection, LABELS, ORGANIC, PLASTIC, PAPER, GLASS_CANS, RESIDUAL, SANITARY, GREEN

def _residual_zone(day: date) -> str:
    anchor = date(2026, 7, 1)  # official calendar reference: South
    weeks = (day - anchor).days // 7
    return ZONE_SOUTH if weeks % 2 == 0 else ZONE_NORTH

def build(zone: str) -> list[Collection]:
    result=[]
    day=date(2026,1,1)
    end=date(2026,12,31)
    while day<=end:
        types=[]
        wd=day.weekday()
        if wd in (0,3): types.append(ORGANIC)
        if wd==1:
            types.append(PLASTIC)
            if 3 <= day.month <= 10 or day.isocalendar().week % 2 == 0: types.append(GREEN)
        if wd==2:
            types.append(GLASS_CANS); types.append(SANITARY)
            if _residual_zone(day)==zone: types.append(RESIDUAL)
        if wd==4: types.append(PAPER)
        if wd==5:
            if 6 <= day.month <= 8: types.append(ORGANIC)
            types.append(SANITARY)
        if types:
            result.append(Collection(day,tuple(types),tuple(LABELS[x] for x in types)))
        day += timedelta(days=1)
    return result
