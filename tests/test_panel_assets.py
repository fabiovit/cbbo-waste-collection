from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"

def test_panel_assets_and_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.1.6"
    assert "frontend" in manifest["dependencies"]
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'customElements.define("cbbo-waste-collection-panel-v216"' in panel
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


def test_v216_suppresses_stale_fallback_error():
    backend = (INTEGRATION / "panel.py").read_text()
    assert 'PANEL_COMPONENT = "cbbo-waste-collection-panel-v216"' in backend
    assert 'else None' in backend
    assert 'startswith("bundled_")' in backend

def test_v216_hacs_info_is_current():
    info = (ROOT / "info.md").read_text()
    assert "versione 2.1.6" in info
    assert "La versione 2.0 supporta" not in info
    assert "Dashboard laterale" in info





def test_v216_hamburger_opens_ha_menu():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'id="ha-menu"' in panel
    assert 'icon="mdi:menu"' in panel
    assert '"hass-toggle-menu"' in panel
    assert 'bubbles: true' in panel
    assert 'composed: true' in panel
    assert '.menu-button{display:none' in panel
    assert '@media(max-width:720px){.menu-button{display:inline-flex}' in panel
    assert 'mdi:view-dashboard' not in panel
    backend = (INTEGRATION / "panel.py").read_text()
    assert 'PANEL_COMPONENT = "cbbo-waste-collection-panel-v216"' in backend
