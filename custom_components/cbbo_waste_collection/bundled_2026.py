"""Bundled 2026 CBBO collection profiles for all supported municipalities.

These profiles are the offline fallback used when the public CBBO page cannot be
parsed.  The online source always has priority.  Profiles are based on the 2026
CBBO municipality calendars and current municipality collection instructions.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Callable

from .const import ZONE_NORTH, ZONE_SOUTH
from .schedule import (
    Collection, LABELS, ORGANIC, PLASTIC, PAPER, GLASS_CANS,
    RESIDUAL, SANITARY, GREEN,
)

YEAR = 2026


def _biweekly(day: date, anchor: date) -> bool:
    return ((day - anchor).days // 7) % 2 == 0


def _add(result: list[Collection], day: date, types: list[str] | tuple[str, ...]) -> None:
    unique = tuple(dict.fromkeys(types))
    if unique:
        result.append(Collection(day, unique, tuple(LABELS[item] for item in unique)))


def _generic(builder: Callable[[date], list[str] | tuple[str, ...]]) -> list[Collection]:
    result: list[Collection] = []
    day = date(YEAR, 1, 1)
    end = date(YEAR, 12, 31)
    while day <= end:
        _add(result, day, builder(day))
        day += timedelta(days=1)
    return result


def _acquafredda(d: date):
    # Official 2026 Ecocalendario: organic Tuesday/Saturday; glass/residual
    # alternate on Monday; paper/plastic alternate on Wednesday.
    t=[]; wd=d.weekday()
    if wd==0: t.append(GLASS_CANS if _biweekly(d,date(2026,7,6)) else RESIDUAL)
    if wd==1: t.append(ORGANIC)
    if wd==2: t.append(PAPER if _biweekly(d,date(2026,7,1)) else PLASTIC)
    if wd==5: t.append(ORGANIC)
    return t


def _barbariga(d: date):
    # CBBO service active from 1 June 2026. The 2026 Ecocalendario confirms
    # organic collection on Wednesday/Saturday and sanitary textiles Thursday.
    if d < date(2026,6,1): return []
    t=[]; wd=d.weekday()
    if wd in (2,5): t.append(ORGANIC)
    if wd==3:
        t.extend((PAPER,SANITARY))
    # The three dry fractions use the Wednesday fortnightly cycle in the
    # post-June 2026 calendar. They are intentionally kept on the same base
    # cycle here; online data remains authoritative for exceptional shifts.
    if wd==2 and _biweekly(d,date(2026,6,3)):
        t.extend((RESIDUAL,PLASTIC,GLASS_CANS))
    return t


def _calvisano(d: date):
    # Official 2026 guide: organic Tue/Sat, glass Tue, plastic Wed,
    # paper Thu, residual + sanitary textiles Fri.
    t=[]; wd=d.weekday()
    if wd==1: t.extend((ORGANIC,GLASS_CANS))
    if wd==2: t.append(PLASTIC)
    if wd==3: t.append(PAPER)
    if wd==4: t.extend((RESIDUAL,SANITARY))
    if wd==5: t.append(ORGANIC)
    return t


def _capriano(d: date):
    # Official service programme: Monday organic/residual/plastic/glass/sanitary,
    # Thursday paper, Friday organic.
    t=[]; wd=d.weekday()
    if wd==0: t.extend((ORGANIC,PLASTIC,RESIDUAL,SANITARY,GLASS_CANS))
    if wd==3: t.append(PAPER)
    if wd==4: t.append(ORGANIC)
    return t


def _carpenedolo(d: date):
    # Official 2026 guide: plastic + sanitary Mon, organic Tue/Sat,
    # residual Wed, paper Thu, glass + sanitary Fri.
    t=[]; wd=d.weekday()
    if wd==0: t.extend((PLASTIC,SANITARY))
    if wd==1: t.append(ORGANIC)
    if wd==2: t.append(RESIDUAL)
    if wd==3: t.append(PAPER)
    if wd==4: t.extend((SANITARY,GLASS_CANS))
    if wd==5: t.append(ORGANIC)
    return t


def _castenedolo(d: date):
    t=[]; wd=d.weekday()
    if wd==0:
        t.append(ORGANIC)
        if 3 <= d.month <= 11: t.append(GREEN)
    if wd==1:
        t.extend((PLASTIC,GLASS_CANS))
    if wd==2: t.append(PAPER)
    if wd==3: t.append(ORGANIC)
    if wd==4: t.extend((RESIDUAL,SANITARY))
    if wd==5 and 6 <= d.month <= 8: t.append(ORGANIC)
    return t


def _flero(d: date):
    # Official 2026 guide: organic Mon/Thu, plastic Mon, sanitary Wed,
    # paper + glass Thu, residual Fri. Green is collected Monday Mar-Nov.
    t=[]; wd=d.weekday()
    if wd==0:
        t.extend((ORGANIC,PLASTIC))
        if 3 <= d.month <= 11: t.append(GREEN)
    if wd==2: t.append(SANITARY)
    if wd==3: t.extend((ORGANIC,PAPER,GLASS_CANS))
    if wd==4: t.append(RESIDUAL)
    return t


def _ghedi(d: date):
    # Current 2026 pattern matches the municipal service programme.
    t=[]; wd=d.weekday()
    if wd==0: t.extend((ORGANIC,PLASTIC))
    if wd==1: t.extend((RESIDUAL,SANITARY))
    if wd==2: t.append(PAPER)
    if wd==3: t.append(ORGANIC)
    if wd==4: t.extend((GLASS_CANS,SANITARY))
    if wd==5 and 6 <= d.month <= 9: t.append(ORGANIC)
    return t


def _isorella(d: date):
    t=[]; wd=d.weekday()
    if wd==0: t.append(ORGANIC)
    if wd==1: t.append(RESIDUAL)
    if wd==2: t.append(PLASTIC)
    if wd==3: t.append(ORGANIC)
    if wd==4: t.append(PAPER if _biweekly(d,date(2026,7,3)) else GLASS_CANS)
    return t


def _mazzano(d: date, zone: str):
    t=[]; wd=d.weekday()
    if wd in (0,3): t.append(ORGANIC)
    if wd==1:
        t.append(PLASTIC)
        if 3 <= d.month <= 10: t.append(GREEN)
    if wd==2:
        t.extend((GLASS_CANS,SANITARY))
        anchor=date(2026,7,1)
        south=_biweekly(d,anchor)
        if (zone==ZONE_SOUTH and south) or (zone==ZONE_NORTH and not south): t.append(RESIDUAL)
    if wd==4: t.append(PAPER)
    if wd==5:
        if 6 <= d.month <= 8: t.append(ORGANIC)
        t.append(SANITARY)
    return t


def _montichiari(d: date):
    t=[]; wd=d.weekday()
    if wd==0: t.append(ORGANIC)
    if wd==1: t.extend((RESIDUAL,SANITARY))
    if wd==2: t.append(GLASS_CANS)
    if wd==3: t.append(ORGANIC)
    if wd==4: t.extend((PAPER,PLASTIC))
    return t


def _montirone(d: date):
    t=[]; wd=d.weekday()
    if wd==0: t.extend((ORGANIC,RESIDUAL,SANITARY))
    if wd==1: t.append(GLASS_CANS)
    if wd==2: t.append(PLASTIC)
    if wd==3: t.append(PAPER)
    if wd==4: t.append(ORGANIC)
    return t


def _nuvolento(d: date):
    # 2026 programme: residual Mon fortnightly; organic Tue/Sat plus Thu in
    # the warm-season three-times-weekly period; paper Thu fortnightly;
    # plastic Fri; glass Fri fortnightly; sanitary Mon/Fri; green Monday.
    t=[]; wd=d.weekday()
    if wd==0:
        t.append(SANITARY)
        if _biweekly(d,date(2026,7,13)): t.append(RESIDUAL)
        if 3 <= d.month <= 10: t.append(GREEN)
    if wd==1: t.append(ORGANIC)
    if wd==3:
        if 5 <= d.month <= 9: t.append(ORGANIC)
        if _biweekly(d,date(2026,7,9)): t.append(PAPER)
    if wd==4:
        t.extend((PLASTIC,SANITARY))
        if _biweekly(d,date(2026,7,10)): t.append(GLASS_CANS)
    if wd==5: t.append(ORGANIC)
    return t


def _nuvolera(d: date):
    # 2026 programme: residual Mon fortnightly; organic Tue/Sat plus Thu in
    # the warm season; paper Thu fortnightly; plastic Fri; glass Fri
    # fortnightly; sanitary Mon/Fri; green Monday Mar-Oct.
    t=[]; wd=d.weekday()
    if wd==0:
        t.append(SANITARY)
        if _biweekly(d,date(2026,7,6)): t.append(RESIDUAL)
        if 3 <= d.month <= 10: t.append(GREEN)
    if wd==1: t.append(ORGANIC)
    if wd==3:
        if 5 <= d.month <= 9: t.append(ORGANIC)
        if _biweekly(d,date(2026,7,2)): t.append(PAPER)
    if wd==4:
        t.extend((PLASTIC,SANITARY))
        if _biweekly(d,date(2026,7,3)): t.append(GLASS_CANS)
    if wd==5: t.append(ORGANIC)
    return t


def _poncarale(d: date):
    t=[]; wd=d.weekday()
    if wd==0:
        t.append(RESIDUAL)
        if 3 <= d.month <= 11: t.append(GREEN)
    if wd==1: t.extend((ORGANIC,GLASS_CANS))
    if wd==2: t.append(PLASTIC)
    if wd==3: t.append(PAPER)
    if wd==4: t.append(ORGANIC)
    return t


def _remedello(d: date):
    # 2026 calendar: organic Monday/Thursday, residual + sanitary Wednesday,
    # paper/plastic alternate on Friday.
    t=[]; wd=d.weekday()
    if wd==0: t.append(ORGANIC)
    if wd==2: t.extend((RESIDUAL,SANITARY))
    if wd==3: t.append(ORGANIC)
    if wd==4: t.append(PAPER if _biweekly(d,date(2026,7,3)) else PLASTIC)
    return t


def _san_zeno(d: date):
    # Organico and residual are collected in street containers with electronic lid;
    # the door-to-door calendar covers the dry recyclable fractions.
    t=[]; wd=d.weekday()
    if wd==0: t.append(PAPER)
    if wd==2: t.append(PLASTIC)
    if wd==3: t.append(GLASS_CANS)
    return t


def _visano(d: date):
    t=[]; wd=d.weekday()
    if wd==0: t.append(RESIDUAL)
    if wd==1: t.append(ORGANIC)
    if wd==2: t.append(PAPER if _biweekly(d,date(2026,7,1)) else PLASTIC)
    if wd==5: t.append(ORGANIC)
    return t


_BUILDERS = {
    "acquafredda": _acquafredda,
    "barbariga": _barbariga,
    "calvisano": _calvisano,
    "capriano-del-colle": _capriano,
    "carpenedolo": _carpenedolo,
    "castenedolo": _castenedolo,
    "flero": _flero,
    "ghedi": _ghedi,
    "isorella": _isorella,
    "montichiari": _montichiari,
    "montirone": _montirone,
    "nuvolento": _nuvolento,
    "nuvolera": _nuvolera,
    "poncarale": _poncarale,
    "remedello": _remedello,
    "san-zeno-naviglio": _san_zeno,
    "visano": _visano,
}


def build(municipality: str, zone: str = "default") -> list[Collection]:
    """Return the bundled 2026 profile for a municipality."""
    if municipality == "mazzano":
        return _generic(lambda d: _mazzano(d, zone))
    builder = _BUILDERS.get(municipality)
    if builder is None:
        return []
    return _generic(builder)
