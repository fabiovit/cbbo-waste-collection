from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "custom_components" / "cbbo_waste_collection" / "recycling_centers.py"

spec = importlib.util.spec_from_file_location("recycling_centers", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_all_supported_municipalities_have_center_data():
    assert len(mod.RECYCLING_CENTERS) == 18


def test_centers_have_required_fields_and_week_schedule():
    for key, center in mod.RECYCLING_CENTERS.items():
        assert center["address"], key
        assert center["official_url"].startswith("https://www.cbbo.it/"), key
        assert center["periods"], key
        for period in center["periods"]:
            assert set(period["schedule"]) == {str(i) for i in range(7)}


def test_seasonal_centers_remain_supported():
    assert len(mod.RECYCLING_CENTERS["mazzano"]["periods"]) == 2
    assert len(mod.RECYCLING_CENTERS["barbariga"]["periods"]) == 2
