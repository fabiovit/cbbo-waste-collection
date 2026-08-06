from datetime import date
import importlib.util,sys,types
from pathlib import Path
BASE=Path(__file__).parents[1]/"custom_components"/"cbbo_waste_collection"
pkg=types.ModuleType("cbbo_waste_collection");pkg.__path__=[str(BASE)];sys.modules["cbbo_waste_collection"]=pkg
for name in ("const","schedule","api"):
    spec=importlib.util.spec_from_file_location(f"cbbo_waste_collection.{name}",BASE/f"{name}.py");mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
from cbbo_waste_collection.api import CBBOApiClient

def test_fullcalendar_json():
    body='<script type="application/json">[{"title":"Organico","start":"2026-08-10"},{"title":"Carta e cartone","start":"2026-08-11"}]</script>'
    events=CBBOApiClient.parse_events(body)
    assert (date(2026,8,10),"Organico",None) in events
    assert (date(2026,8,11),"Carta e cartone",None) in events

def test_html_data_date():
    events=CBBOApiClient.parse_events('<div data-date="2026-08-12"><span>Vetro e lattine</span></div>')
    assert (date(2026,8,12),"Vetro e lattine",None) in events

def test_js_object():
    events=CBBOApiClient.parse_events("events=[{title:'Plastica', start:'2026-08-13'}]")
    assert (date(2026,8,13),"Plastica",None) in events
