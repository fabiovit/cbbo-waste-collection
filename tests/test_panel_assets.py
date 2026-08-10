from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_panel_assets_and_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.1.2"
    assert "frontend" in manifest["dependencies"]
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'customElements.define("cbbo-waste-collection-panel"' in panel
    assert "cbbo_waste_collection/panel_data" in panel

def test_panel_backend_registered():
    panel = (INTEGRATION / "panel.py").read_text()
    assert 'PANEL_URL_PATH = "cbbo-waste-collection"' in panel
    assert "panel_custom.async_register_panel" in panel
    assert "async_register_static_paths" in panel
    assert "module_url=" in panel
    assert "frontend.add_extra_js_url" not in panel
    assert 'f"{DOMAIN}/panel_data"' in panel

def test_panel_hides_fallback_parser_error():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'entry.source_status === "online"' in panel
    assert 'Local 2026 calendar active' in panel
    backend = (INTEGRATION / "panel.py").read_text()
    assert '"source_status": (' in backend
    assert 'startswith("bundled_")' in backend
