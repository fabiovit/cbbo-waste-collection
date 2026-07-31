"""Models and helpers for CBBO waste collections."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

ORGANIC = "organic"
PLASTIC = "plastic"
PAPER = "paper"
GLASS_CANS = "glass_cans"
RESIDUAL = "residual"
SANITARY = "sanitary"
GREEN = "green"
OTHER = "other"

LABELS = {
    ORGANIC: "Frazione organica",
    PLASTIC: "Imballaggi in plastica",
    PAPER: "Carta e cartone",
    GLASS_CANS: "Vetro e lattine",
    RESIDUAL: "Rifiuti non differenziabili",
    SANITARY: "Tessili sanitari",
    GREEN: "Verde",
    OTHER: "Altro",
}

ICONS = {
    ORGANIC: "mdi:food-apple",
    PLASTIC: "mdi:bottle-soda",
    PAPER: "mdi:package-variant",
    GLASS_CANS: "mdi:bottle-wine",
    RESIDUAL: "mdi:trash-can",
    SANITARY: "mdi:baby-face-outline",
    GREEN: "mdi:leaf",
    OTHER: "mdi:recycle",
}

TITLE_MAP = {
    "frazione organica": ORGANIC,
    "organico": ORGANIC,
    "imballaggi in plastica": PLASTIC,
    "plastica": PLASTIC,
    "carta e cartone": PAPER,
    "carta": PAPER,
    "vetro": GLASS_CANS,
    "vetro e lattine": GLASS_CANS,
    "rifiuti non differenziabili": RESIDUAL,
    "rifiuto non riciclabile": RESIDUAL,
    "indifferenziato": RESIDUAL,
    "tessili sanitari": SANITARY,
    "verde": GREEN,
    "sfalci e ramaglie": GREEN,
}


@dataclass(frozen=True, slots=True)
class Collection:
    """One collection day."""

    day: date
    waste_types: tuple[str, ...]
    labels: tuple[str, ...]


def normalize_title(title: str) -> tuple[str, str]:
    """Map a source title to an internal waste type and clean label."""
    clean = " ".join(title.replace("&amp;", "&").split()).strip(" -–—")
    key = clean.casefold()
    for source, waste_type in TITLE_MAP.items():
        if source in key:
            return waste_type, LABELS[waste_type]
    return OTHER, clean or LABELS[OTHER]
