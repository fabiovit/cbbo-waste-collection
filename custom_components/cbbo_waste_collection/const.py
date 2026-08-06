"""Constants for CBBO Waste Collection."""
from __future__ import annotations

from datetime import timedelta

DOMAIN = "cbbo_waste_collection"
PLATFORMS = ["sensor", "binary_sensor", "calendar"]

CONF_MUNICIPALITY = "municipality"
CONF_ZONE = "zone"
CONF_INCLUDE_GREEN = "include_green"
CONF_INCLUDE_SANITARY = "include_sanitary"

ZONE_DEFAULT = "default"
ZONE_NORTH = "north"
ZONE_SOUTH = "south"

MUNICIPALITIES: dict[str, str] = {
    "acquafredda": "Acquafredda", "barbariga": "Barbariga", "calvisano": "Calvisano",
    "capriano-del-colle": "Capriano del Colle", "carpenedolo": "Carpenedolo",
    "castenedolo": "Castenedolo", "flero": "Flero", "ghedi": "Ghedi",
    "isorella": "Isorella", "mazzano": "Mazzano", "montichiari": "Montichiari",
    "montirone": "Montirone", "nuvolento": "Nuvolento", "nuvolera": "Nuvolera",
    "poncarale": "Poncarale", "remedello": "Remedello",
    "san-zeno-naviglio": "San Zeno Naviglio", "visano": "Visano",
}
MUNICIPALITY_ZONES: dict[str, dict[str, str]] = {
    "mazzano": {ZONE_NORTH: "Zona Nord", ZONE_SOUTH: "Zona Sud"},
}
BASE_URL = "https://www.cbbo.it"
CACHE_VERSION = 1
UPDATE_INTERVAL = timedelta(hours=6)
SERVICE_REFRESH = "refresh"
SERVICE_CLEAR_CACHE = "clear_cache"
