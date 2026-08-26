"""Collection models and waste-title normalization."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Final

ORGANIC: Final = "organic"
PLASTIC: Final = "plastic"
PAPER: Final = "paper"
GLASS_CANS: Final = "glass_cans"
RESIDUAL: Final = "residual"
SANITARY: Final = "sanitary"
GREEN: Final = "green"
OTHER: Final = "other"

LABELS: Final[dict[str, str]] = {
    ORGANIC: "Frazione organica",
    PLASTIC: "Imballaggi in plastica",
    PAPER: "Carta e cartone",
    GLASS_CANS: "Vetro e lattine",
    RESIDUAL: "Rifiuti non differenziabili",
    SANITARY: "Tessili sanitari",
    GREEN: "Verde",
    OTHER: "Altro",
}

ICONS: Final[dict[str, str]] = {
    ORGANIC: "mdi:food-apple",
    PLASTIC: "mdi:bottle-soda",
    PAPER: "mdi:package-variant",
    GLASS_CANS: "mdi:bottle-wine",
    RESIDUAL: "mdi:trash-can",
    SANITARY: "mdi:baby-face-outline",
    GREEN: "mdi:leaf",
    OTHER: "mdi:recycle",
}

PATTERNS: Final[tuple[tuple[str, str], ...]] = (
    (r"frazione organica|\borganico\b|umido", ORGANIC),
    (r"imballaggi? in plastica|\bplastica\b", PLASTIC),
    (r"carta e cartone|\bcarta\b|cartone", PAPER),
    (r"vetro e lattine|vetro.*lattine|\bvetro\b|lattine", GLASS_CANS),
    (
        r"rifiut[oi] non differenziabil|rifiut[oi] non riciclabil|"
        r"indifferenziat|secco residuo",
        RESIDUAL,
    ),
    (r"tessili sanitari|pannolini|pannoloni", SANITARY),
    (r"sfalci e ramaglie|\bverde\b", GREEN),
)


@dataclass(frozen=True, slots=True)
class Collection:
    """One collection date and all waste types collected on that date."""

    day: date
    waste_types: tuple[str, ...]
    labels: tuple[str, ...]


def normalize_title(title: str) -> tuple[str, str]:
    """Normalize a CBBO event title to a stable waste type and label."""
    clean = " ".join(
        re.sub(r"<[^>]+>", " ", title).replace("&amp;", "&").split()
    ).strip(" -–—")
    lowered = clean.casefold()

    for pattern, waste_type in PATTERNS:
        if re.search(pattern, lowered):
            return waste_type, LABELS[waste_type]

    return OTHER, clean or LABELS[OTHER]
