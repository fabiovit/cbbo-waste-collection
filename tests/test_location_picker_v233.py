from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.3.3"

def test_only_configured_entries_are_rendered():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "const entries=this._data?.entries||[]" in panel
    assert "entries.map(x=>" in panel
    assert "municipalities" not in panel
    assert "update_location" not in panel

def test_modern_location_picker():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'id="location-picker-trigger"' in panel
    assert 'class="location-picker-menu"' in panel
    assert ".location-picker.open .location-picker-menu{display:block}" in panel
    assert ".location-option" in panel
    assert "aria-expanded" in panel
    assert '<select class="select" id="entry-select">' not in panel

def test_selection_is_local_dashboard_profile_only():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "localStorage.setItem('cbbo-panel-entry',entryId)" in panel
    assert "this._selectedEntryId=entryId" in panel
