from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.3.5"

def test_large_waste_icons():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert ".waste-token ha-icon{--mdc-icon-size:42px}" in panel
    assert ".waste-dot ha-icon{--mdc-icon-size:30px}" in panel
    assert ".rail-dots .waste-dot ha-icon{--mdc-icon-size:25px}" in panel
    assert "a colpo d’occhio" in panel
