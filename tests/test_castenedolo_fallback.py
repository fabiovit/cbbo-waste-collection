from datetime import date
import importlib.util,sys,types
from pathlib import Path
BASE=Path(__file__).parents[1]/"custom_components"/"cbbo_waste_collection"
pkg=sys.modules.get("cbbo_waste_collection")
if pkg is None:
    pkg=types.ModuleType("cbbo_waste_collection");pkg.__path__=[str(BASE)];sys.modules["cbbo_waste_collection"]=pkg
for name in ("schedule","castenedolo_fallback"):
    key=f"cbbo_waste_collection.{name}"
    if key not in sys.modules:
        spec=importlib.util.spec_from_file_location(key,BASE/f"{name}.py");mod=importlib.util.module_from_spec(spec);sys.modules[key]=mod;spec.loader.exec_module(mod)
from cbbo_waste_collection.castenedolo_fallback import build
from cbbo_waste_collection.schedule import GLASS_CANS, ORGANIC, PAPER, PLASTIC, RESIDUAL, SANITARY

def by_day(): return {item.day:item for item in build()}

def test_castenedolo_regular_week_august():
    data=by_day()
    assert data[date(2026,8,3)].waste_types==(ORGANIC,)
    assert data[date(2026,8,4)].waste_types==(PLASTIC,GLASS_CANS)
    assert data[date(2026,8,5)].waste_types==(PAPER,)
    assert data[date(2026,8,6)].waste_types==(ORGANIC,)
    assert data[date(2026,8,7)].waste_types==(RESIDUAL,SANITARY)

def test_castenedolo_new_year_variations():
    data=by_day()
    assert date(2026,1,1) not in data
    assert data[date(2026,1,2)].waste_types==(ORGANIC,)
    assert data[date(2026,1,3)].waste_types==(RESIDUAL,SANITARY)
