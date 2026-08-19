from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "custom_components" / "cbbo_waste_collection" / "frontend" / "cbbo-panel.js"

def test_bilingual_ui():
    text = PANEL.read_text()
    assert "const I18N" in text
    assert 'it: {' in text
    assert 'en: {' in text
    assert "data-lang=\"it\"" in text
    assert "data-lang=\"en\"" in text

def test_recycling_center_view():
    text = PANEL.read_text()
    assert "centerView(e)" in text
    assert "centerStatus(center)" in text
    assert "Recycling Center" in text
    assert "Centro di raccolta" in text

def test_sanitary_waste_wording():
    text = PANEL.read_text()
    assert "pannolini e pannoloni" in text
    assert "diapers & incontinence products" in text
