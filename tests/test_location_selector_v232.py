from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.3.2"

def test_backend_location_update():
    panel = (INTEGRATION / "panel.py").read_text()
    assert 'f"{DOMAIN}/update_location"' in panel
    assert "@websocket_api.require_admin" in panel
    assert "async_update_entry(" in panel
    assert "async_reload(entry.entry_id)" in panel
    assert '"municipalities": [' in panel
    assert '"zones": MUNICIPALITY_ZONES' in panel

def test_frontend_location_controls():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'id="municipality-select"' in panel
    assert 'id="zone-select"' in panel
    assert 'id="save-location"' in panel
    assert "async updateLocation(entryId,municipality,zone)" in panel
    assert "cbbo_waste_collection/update_location" in panel
    assert "Salva Comune" in panel
