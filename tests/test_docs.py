from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_is_bilingual_and_has_screenshots():
    readme = (ROOT / "README.md").read_text()
    assert "## 🇮🇹 Italiano" in readme
    assert "## 🇬🇧 English" in readme
    assert "docs/screenshots/overview.png" in readme
    assert "docs/screenshots/municipality.png" in readme


def test_hacs_info_is_current():
    info = (ROOT / "info.md").read_text()
    assert "3.0.0" in info
    assert "Italiano" in info
    assert "English" in info


def test_marketplace_documentation_and_badge():
    readme = (ROOT / "README.md").read_text()
    assert "marketplace_repository/?owner=fabiovit&repository=cbbo-waste-collection&category=integration" in readme
    assert "Add from link" in readme
    assert "Home Assistant 2026.11+" in readme
    assert "Home Assistant 2026.10" in readme
    assert "## 🇮🇹 Italiano" in readme
    assert "## 🇬🇧 English" in readme
