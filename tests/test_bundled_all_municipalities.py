from datetime import date
import importlib.util,sys,types
from pathlib import Path
BASE=Path(__file__).parents[1]/"custom_components"/"cbbo_waste_collection"
if "cbbo_waste_collection" not in sys.modules:
    pkg=types.ModuleType("cbbo_waste_collection");pkg.__path__=[str(BASE)];sys.modules["cbbo_waste_collection"]=pkg
for name in ("const","schedule","bundled_2026"):
    fq=f"cbbo_waste_collection.{name}"
    if fq not in sys.modules:
        spec=importlib.util.spec_from_file_location(fq,BASE/f"{name}.py");mod=importlib.util.module_from_spec(spec);sys.modules[fq]=mod;spec.loader.exec_module(mod)
from cbbo_waste_collection.bundled_2026 import build
from cbbo_waste_collection.const import MUNICIPALITIES, ZONE_SOUTH
from cbbo_waste_collection.schedule import (
    ORGANIC, PLASTIC, PAPER, GLASS_CANS, RESIDUAL, SANITARY, GREEN
)


def _types(municipality, day, zone="default"):
    for item in build(municipality, zone):
        if item.day == day:
            return item.waste_types
    return ()


def test_all_municipalities_have_2026_fallback():
    for municipality in MUNICIPALITIES:
        zone = ZONE_SOUTH if municipality == "mazzano" else "default"
        data = build(municipality, zone)
        assert data, municipality
        assert all(item.day.year == 2026 for item in data)
        assert data == sorted(data, key=lambda item: item.day)


def test_august_7_2026_matrix_all_municipalities():
    """Regression matrix checked against CBBO 2026 municipality calendars."""
    d=date(2026,8,7)  # Friday
    expected={
        "acquafredda": (),
        "barbariga": (),
        "calvisano": (RESIDUAL,SANITARY),
        "capriano-del-colle": (ORGANIC,),
        "carpenedolo": (SANITARY,GLASS_CANS),
        "castenedolo": (RESIDUAL,SANITARY),
        "flero": (RESIDUAL,),
        "ghedi": (GLASS_CANS,SANITARY),
        "isorella": (),
        "mazzano": (PAPER,),
        "montichiari": (PAPER,),
        "montirone": (),
        "nuvolento": (PLASTIC,SANITARY,GLASS_CANS),
        "nuvolera": (PLASTIC,SANITARY),
        "poncarale": (),
        "remedello": (PLASTIC,),
        "san-zeno-naviglio": (),
        "visano": (),
    }
    for municipality, wanted in expected.items():
        zone=ZONE_SOUTH if municipality=="mazzano" else "default"
        assert _types(municipality,d,zone)==wanted, municipality


def test_carpenedolo_week_is_exact():
    assert _types("carpenedolo",date(2026,8,3))==(PLASTIC,SANITARY)
    assert _types("carpenedolo",date(2026,8,4))==(ORGANIC,)
    assert _types("carpenedolo",date(2026,8,5))==(RESIDUAL,)
    assert _types("carpenedolo",date(2026,8,6))==(PAPER,)
    assert _types("carpenedolo",date(2026,8,7))==(SANITARY,GLASS_CANS)
    assert _types("carpenedolo",date(2026,8,8))==(ORGANIC,)


def test_calvisano_week_is_exact():
    assert _types("calvisano",date(2026,8,3))==()
    assert _types("calvisano",date(2026,8,4))==(ORGANIC,GLASS_CANS)
    assert _types("calvisano",date(2026,8,5))==(PLASTIC,)
    assert _types("calvisano",date(2026,8,6))==(PAPER,)
    assert _types("calvisano",date(2026,8,7))==(RESIDUAL,SANITARY)
    assert _types("calvisano",date(2026,8,8))==(ORGANIC,)


def test_flero_week_is_exact():
    mon=_types("flero",date(2026,8,3))
    assert mon==(ORGANIC,PLASTIC,GREEN)
    assert _types("flero",date(2026,8,4))==()
    assert _types("flero",date(2026,8,5))==(SANITARY,)
    assert _types("flero",date(2026,8,6))==(ORGANIC,PAPER,GLASS_CANS)
    assert _types("flero",date(2026,8,7))==(RESIDUAL,)


def test_capriano_paper_is_thursday():
    assert PAPER not in _types("capriano-del-colle",date(2026,8,5))
    assert _types("capriano-del-colle",date(2026,8,6))==(PAPER,)


def test_castenedolo_tuesday_has_no_sanitary():
    tue=_types("castenedolo",date(2026,8,4))
    assert tue==(PLASTIC,GLASS_CANS)
    assert SANITARY not in tue


def test_acquafredda_organic_is_tuesday_and_saturday():
    assert _types("acquafredda",date(2026,8,4))==(ORGANIC,)
    assert _types("acquafredda",date(2026,8,7))==()
    assert _types("acquafredda",date(2026,8,8))==(ORGANIC,)


def test_nuvolera_friday_cycle():
    # Glass was collected on 3/17/31 July, so 7 Aug is plastic + sanitary only.
    assert _types("nuvolera",date(2026,7,31))==(PLASTIC,SANITARY,GLASS_CANS)
    assert _types("nuvolera",date(2026,8,7))==(PLASTIC,SANITARY)


def test_nuvolento_friday_cycle():
    # Nuvolento's glass phase is offset by one week relative to Nuvolera.
    assert _types("nuvolento",date(2026,8,7))==(PLASTIC,SANITARY,GLASS_CANS)


def test_barbariga_starts_june_2026():
    data=build("barbariga")
    assert min(x.day for x in data)>=date(2026,6,1)


def test_ghedi_current_pattern():
    assert _types("ghedi",date(2026,8,3))==(ORGANIC,PLASTIC)
    assert _types("ghedi",date(2026,8,4))==(RESIDUAL,SANITARY)
    assert _types("ghedi",date(2026,8,7))==(GLASS_CANS,SANITARY)


def test_mazzano_south_august_7_paper():
    assert _types("mazzano",date(2026,8,7),ZONE_SOUTH)==(PAPER,)


def test_v202_reported_calendar_corrections():
    d=date(2026,8,7)
    assert _types("isorella",d)==()
    assert _types("montichiari",d)==(PAPER,)
    assert _types("montirone",d)==()
    assert _types("poncarale",d)==()
    assert _types("poncarale",date(2026,8,8))==(PAPER,ORGANIC)
    assert _types("san-zeno-naviglio",date(2026,8,10))==(PAPER,GLASS_CANS)
