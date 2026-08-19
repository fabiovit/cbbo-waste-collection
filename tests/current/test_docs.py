from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_bilingual_readme_and_screenshots():
    readme = (ROOT / "README.md").read_text()
    assert "## 🇮🇹 Italiano" in readme
    assert "## English" in readme
    assert "docs/screenshots/overview.png" in readme
    assert "docs/screenshots/municipality.png" in readme
    assert (ROOT / "docs" / "screenshots" / "overview.png").exists()
    assert (ROOT / "docs" / "screenshots" / "municipality.png").exists()
