import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "custom_components" / "cbbo_waste_collection" / "schedule.py"

spec = importlib.util.spec_from_file_location("schedule", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_common_waste_titles_are_normalized():
    cases = {
        "Frazione organica": mod.ORGANIC,
        "Carta e Cartone": mod.PAPER,
        "Imballaggi in plastica": mod.PLASTIC,
        "Vetro e lattine": mod.GLASS_CANS,
        "Rifiuti non differenziabili": mod.RESIDUAL,
        "Tessili sanitari - pannolini": mod.SANITARY,
        "Sfalci e ramaglie": mod.GREEN,
    }
    for title, expected in cases.items():
        assert mod.normalize_title(title)[0] == expected
