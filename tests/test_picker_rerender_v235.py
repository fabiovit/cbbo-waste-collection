from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.3.5"

def test_picker_state_is_persistent():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "this._locationPickerOpen=false;" in panel
    assert "const willOpen=!this._locationPickerOpen;" in panel
    assert "this._locationPickerOpen=willOpen;" in panel
    assert "this._locationPickerOpen?'open':''" in panel

def test_hass_updates_do_not_destroy_open_picker():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "else if(!(this._view==='place' && this._locationPickerOpen))" in panel
    assert "if(!(this._view==='place'&&this._locationPickerOpen))this.renderMain()" in panel

def test_selection_closes_picker_intentionally():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "this._locationPickerOpen=false;" in panel
    assert "localStorage.setItem('cbbo-panel-entry',entryId)" in panel

def test_only_configured_profiles_are_listed():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "const entries=this._data?.entries||[]" in panel
    assert "entries.map(x=>" in panel
