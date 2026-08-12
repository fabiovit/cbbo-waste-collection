from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.3.5"

def test_ios_picker_does_not_auto_close():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "document.addEventListener('click',closePicker" not in panel
    assert "setTimeout(()=>document.addEventListener" not in panel
    assert "picker.classList.toggle('open',willOpen)" in panel
    assert "touch-action:manipulation" in panel

def test_picker_closes_on_actual_selection():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "picker?.classList.remove('open')" in panel
    assert "localStorage.setItem('cbbo-panel-entry',entryId)" in panel

def test_only_configured_profiles_remain():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "const entries=this._data?.entries||[]" in panel
    assert "entries.map(x=>" in panel
