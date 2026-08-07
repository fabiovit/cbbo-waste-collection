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
from cbbo_waste_collection.schedule import PAPER, RESIDUAL, SANITARY


def test_all_municipalities_have_2026_fallback():
    for municipality in MUNICIPALITIES:
        zone = ZONE_SOUTH if municipality == "mazzano" else "default"
        data = build(municipality, zone)
        assert data, municipality
        assert all(item.day.year == 2026 for item in data)
        assert data == sorted(data, key=lambda item: item.day)


def test_castenedolo_august_7_matches_live_test():
    item = next(x for x in build("castenedolo") if x.day == date(2026, 8, 7))
    assert RESIDUAL in item.waste_types
    assert SANITARY in item.waste_types


def test_mazzano_south_august_7_paper():
    item = next(x for x in build("mazzano", ZONE_SOUTH) if x.day == date(2026, 8, 7))
    assert PAPER in item.waste_types


def test_barbariga_starts_june_2026():
    data = build("barbariga")
    assert min(x.day for x in data) >= date(2026, 6, 1)


def _types(municipality, day, zone='default'):
    return next(x.waste_types for x in build(municipality, zone) if x.day == day)


def test_flero_july_2026_pattern():
    from cbbo_waste_collection.schedule import ORGANIC, GREEN, PLASTIC, SANITARY, GLASS_CANS
    assert ORGANIC in _types('flero', date(2026,7,6))
    assert GREEN in _types('flero', date(2026,7,6))
    assert PLASTIC in _types('flero', date(2026,7,7))
    assert SANITARY in _types('flero', date(2026,7,8))
    assert GLASS_CANS in _types('flero', date(2026,7,10))


def test_ghedi_july_2026_pattern():
    from cbbo_waste_collection.schedule import ORGANIC, PLASTIC, RESIDUAL, SANITARY, GLASS_CANS
    monday=_types('ghedi', date(2026,7,6))
    assert ORGANIC in monday and PLASTIC in monday
    tuesday=_types('ghedi', date(2026,7,7))
    assert RESIDUAL in tuesday and SANITARY in tuesday
    friday=_types('ghedi', date(2026,7,10))
    assert GLASS_CANS in friday and SANITARY in friday


def test_nuvolento_july_2026_pattern():
    from cbbo_waste_collection.schedule import PAPER, PLASTIC, GLASS_CANS
    assert PAPER in _types('nuvolento', date(2026,7,9))
    friday=_types('nuvolento', date(2026,7,10))
    assert PLASTIC in friday and GLASS_CANS in friday


def test_remedello_july_2026_pattern():
    from cbbo_waste_collection.schedule import ORGANIC, RESIDUAL, SANITARY, PAPER, PLASTIC
    assert ORGANIC in _types('remedello', date(2026,7,6))
    wed=_types('remedello', date(2026,7,8))
    assert RESIDUAL in wed and SANITARY in wed
    assert PAPER in _types('remedello', date(2026,7,3))
    assert PLASTIC in _types('remedello', date(2026,7,10))


def test_visano_organic_is_tuesday_and_saturday():
    from cbbo_waste_collection.schedule import ORGANIC
    assert ORGANIC in _types('visano', date(2026,7,7))
    assert ORGANIC in _types('visano', date(2026,7,11))
