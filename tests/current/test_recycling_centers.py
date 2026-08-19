from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "custom_components" / "cbbo_waste_collection" / "recycling_centers.py"

spec = importlib.util.spec_from_file_location("recycling_centers", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_all_18_municipalities_have_center_data():
    assert len(mod.RECYCLING_CENTERS) == 18

def test_every_center_has_address_source_and_schedule():
    for key, center in mod.RECYCLING_CENTERS.items():
        assert center["address"], key
        assert center["official_url"].startswith("https://www.cbbo.it/"), key
        assert center["periods"], key
        for period in center["periods"]:
            assert "start" in period and "end" in period
            assert set(period["schedule"]) == {str(i) for i in range(7)}

def test_seasonal_centers_present():
    assert len(mod.RECYCLING_CENTERS["mazzano"]["periods"]) == 2
    assert len(mod.RECYCLING_CENTERS["barbariga"]["periods"]) == 2
