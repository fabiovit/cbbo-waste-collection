"""Constants for CBBO Waste Collection."""

DOMAIN = "cbbo_waste_collection"
PLATFORMS = ["sensor", "binary_sensor", "calendar"]

CONF_MUNICIPALITY = "municipality"
CONF_ZONE = "zone"
CONF_INCLUDE_GREEN = "include_green"
CONF_INCLUDE_SANITARY = "include_sanitary"

MUNICIPALITY_MAZZANO = "mazzano"
ZONE_NORTH = "north"
ZONE_SOUTH = "south"

SOURCE_URL = "https://www.cbbo.it/mazzano"
CALENDAR_URL_2026 = "https://www.cbbo.it/sites/default/files/2025-12/Ecocalendario_2026_MAZZANO_WEB.pdf"
