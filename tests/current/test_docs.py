from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_readme_is_bilingual():
    readme = (ROOT / "README.md").read_text()
    assert "## 🇮🇹 Italiano" in readme
    assert "## 🇬🇧 English" in readme
    assert "docs/screenshots/overview.png" in readme
    assert "docs/screenshots/municipality.png" in readme

def test_hacs_info_is_current():
    info = (ROOT / "info.md").read_text()
    assert "2.4.1" in info
    assert "Italiano" in info
    assert "English" in info


def test_language_navigation_links():
    readme = (ROOT / "README.md").read_text()
    assert "[🇬🇧 English](#-english)" in readme
    assert "[🇮🇹 Italiano](#-italiano)" in readme
