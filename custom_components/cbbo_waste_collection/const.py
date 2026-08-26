"""Constants for CBBO Waste Collection."""
from __future__ import annotations

from datetime import timedelta
from typing import Final

DOMAIN: Final = "cbbo_waste_collection"
PLATFORMS: Final = ["sensor", "binary_sensor", "calendar"]

CONF_MUNICIPALITY: Final = "municipality"
CONF_ZONE: Final = "zone"
CONF_INCLUDE_GREEN: Final = "include_green"
CONF_INCLUDE_SANITARY: Final = "include_sanitary"

ZONE_DEFAULT: Final = "default"
ZONE_NORTH: Final = "north"
ZONE_SOUTH: Final = "south"

MUNICIPALITIES: Final[dict[str, str]] = {
    "acquafredda": "Acquafredda",
    "barbariga": "Barbariga",
    "calvisano": "Calvisano",
    "capriano-del-colle": "Capriano del Colle",
    "carpenedolo": "Carpenedolo",
    "castenedolo": "Castenedolo",
    "flero": "Flero",
    "ghedi": "Ghedi",
    "isorella": "Isorella",
    "mazzano": "Mazzano",
    "montichiari": "Montichiari",
    "montirone": "Montirone",
    "nuvolento": "Nuvolento",
    "nuvolera": "Nuvolera",
    "poncarale": "Poncarale",
    "remedello": "Remedello",
    "san-zeno-naviglio": "San Zeno Naviglio",
    "visano": "Visano",
}

MUNICIPALITY_ZONES: Final[dict[str, dict[str, str]]] = {
    "mazzano": {
        ZONE_NORTH: "Zona Nord",
        ZONE_SOUTH: "Zona Sud",
    }
}

BASE_URL: Final = "https://www.cbbo.it"
CACHE_VERSION: Final = 2
UPDATE_INTERVAL: Final = timedelta(hours=6)
SERVICE_REFRESH: Final = "refresh"
SERVICE_CLEAR_CACHE: Final = "clear_cache"
