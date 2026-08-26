from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "cbbo_waste_collection" / "frontend" / "cbbo-panel.js"


def test_bilingual_ui_and_views():
    text = PANEL.read_text()
    assert "const I18N" in text
    assert 'it: {' in text
    assert 'en: {' in text
    assert "centerView(e)" in text
    assert "supportView(e)" in text
    assert "this.tab('center'" in text


def test_location_picker_stability_guard():
    text = PANEL.read_text()
    assert "this._locationPickerOpen=false;" in text
    assert "this._view==='place' && this._locationPickerOpen" in text


def test_panel_styles_are_defined_once():
    text = PANEL.read_text()
    assert "const PANEL_STYLES = `" in text
    assert "const sourceStyle = `" not in text
    assert "querySelector('style')?.textContent" not in text


def test_sanitary_waste_wording():
    text = PANEL.read_text()
    assert "pannolini e pannoloni" in text
    assert "diapers & incontinence products" in text
