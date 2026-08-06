"""Models and waste-title normalisation."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import re

ORGANIC="organic"; PLASTIC="plastic"; PAPER="paper"; GLASS_CANS="glass_cans"
RESIDUAL="residual"; SANITARY="sanitary"; GREEN="green"; OTHER="other"
LABELS={ORGANIC:"Frazione organica",PLASTIC:"Imballaggi in plastica",PAPER:"Carta e cartone",
GLASS_CANS:"Vetro e lattine",RESIDUAL:"Rifiuti non differenziabili",SANITARY:"Tessili sanitari",
GREEN:"Verde",OTHER:"Altro"}
ICONS={ORGANIC:"mdi:food-apple",PLASTIC:"mdi:bottle-soda",PAPER:"mdi:package-variant",
GLASS_CANS:"mdi:bottle-wine",RESIDUAL:"mdi:trash-can",SANITARY:"mdi:baby-face-outline",
GREEN:"mdi:leaf",OTHER:"mdi:recycle"}
PATTERNS=((r"frazione organica|\borganico\b|umido",ORGANIC),(r"imballaggi? in plastica|\bplastica\b",PLASTIC),
(r"carta e cartone|\bcarta\b|cartone",PAPER),(r"vetro e lattine|vetro.*lattine|\bvetro\b|lattine",GLASS_CANS),
(r"rifiut[oi] non differenziabil|rifiut[oi] non riciclabil|indifferenziat|secco residuo",RESIDUAL),
(r"tessili sanitari|pannolini|pannoloni",SANITARY),(r"sfalci e ramaglie|\bverde\b",GREEN))

@dataclass(frozen=True,slots=True)
class Collection:
    day: date
    waste_types: tuple[str,...]
    labels: tuple[str,...]

def normalize_title(title:str)->tuple[str,str]:
    clean=" ".join(re.sub(r"<[^>]+>"," ",title).replace("&amp;","&").split()).strip(" -–—")
    low=clean.casefold()
    for pattern,waste_type in PATTERNS:
        if re.search(pattern,low): return waste_type,LABELS[waste_type]
    return OTHER, clean or LABELS[OTHER]
