from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_release_version_consistency():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    panel_py = (INTEGRATION / "panel.py").read_text()
    panel_js = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()

    assert manifest["version"] == "2.3.5"
    assert '"version": "2.3.5"' in panel_py
    assert "?v=2.3.5" in panel_py
    assert 'CBBO_PANEL_VERSION = "2.3.5"' in panel_js
    assert "cbbo-waste-collection-panel-v235" in panel_js
