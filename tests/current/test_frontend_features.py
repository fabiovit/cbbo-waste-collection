from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "custom_components" / "cbbo_waste_collection" / "frontend" / "cbbo-panel.js"

def test_bilingual_ui():
    text = PANEL.read_text()
    assert "const I18N" in text
    assert 'it: {' in text
    assert 'en: {' in text
    assert 'data-lang="it"' in text
    assert 'data-lang="en"' in text

def test_recycling_center_view():
    text = PANEL.read_text()
    assert "centerView(e)" in text
    assert "centerStatus(center)" in text
    assert "Centro di raccolta" in text
    assert "Recycling Center" in text

def test_location_picker_persists():
    text = PANEL.read_text()
    assert "this._locationPickerOpen=false;" in text
    assert "this._view==='place' && this._locationPickerOpen" in text

def test_sanitary_waste_wording():
    text = PANEL.read_text()
    assert "pannolini e pannoloni" in text
    assert "diapers & incontinence products" in text
