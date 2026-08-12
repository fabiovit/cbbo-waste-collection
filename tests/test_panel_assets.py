from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"


def test_panel_assets_and_version():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text())
    assert manifest["version"] == "2.3.0"
    assert "frontend" in manifest["dependencies"]
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert "cbbo-waste-collection-panel-v230" in panel
    assert "cbbo_waste_collection/panel_data" in panel


def test_panel_backend_registered():
    panel = (INTEGRATION / "panel.py").read_text()
    assert 'PANEL_URL_PATH = "cbbo-waste-collection"' in panel
    assert "panel_custom.async_register_panel" in panel
    assert "async_register_static_paths" in panel
    assert "module_url=" in panel
    assert 'f"{DOMAIN}/panel_data"' in panel


def test_fallback_parser_error_is_suppressed_by_backend():
    backend = (INTEGRATION / "panel.py").read_text()
    assert '"source_status": (' in backend
    assert 'startswith("bundled_")' in backend
    assert '"last_error": (' in backend
    assert "else None" in backend


def test_hacs_info_is_current():
    info = (ROOT / "info.md").read_text()
    assert "2.3.0" in info
    assert "La versione 2.0 supporta" not in info
    assert "Dashboard laterale" in info


def test_hamburger_opens_ha_menu_in_inverter_style_shell():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'id="ha-menu-toggle"' in panel
    assert 'icon="mdi:menu"' in panel
    assert "hass-toggle-menu" in panel
    assert "bubbles:true" in panel
    assert "composed:true" in panel
    assert ".menu-btn{display:none" in panel
    assert "@media(max-width:620px)" in panel
    assert ".menu-btn{display:flex}" in panel


def test_v230_inverter_style_shell_and_views():
    panel = (INTEGRATION / "frontend" / "cbbo-panel.js").read_text()
    assert 'class="topbar"' in panel
    assert 'class="nav-scroller"' in panel
    assert "this.tab('home'" in panel
    assert "this.tab('calendar'" in panel
    assert "this.tab('place'" in panel
    assert "this.tab('diag'" in panel
    assert "Supporta il progetto" in panel
    assert 'class="hero"' in panel
    assert 'class="timeline"' in panel
    assert "supportView(e)" in panel
    backend = (INTEGRATION / "panel.py").read_text()
    assert 'PANEL_COMPONENT = "cbbo-waste-collection-panel-v230"' in backend
