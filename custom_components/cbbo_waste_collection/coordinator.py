"""Coordinator for CBBO Waste Collection."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import CONF_INCLUDE_GREEN, CONF_INCLUDE_SANITARY, CONF_ZONE, DOMAIN
from .schedule import collections_for_day, next_collection, upcoming_collections


class CBBOWasteCoordinator(DataUpdateCoordinator[dict]):
    """Calculate collection information shared by all entities."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self) -> dict:
        today = dt_util.now().date()
        zone = self.entry.data[CONF_ZONE]
        include_green = self.entry.options.get(
            CONF_INCLUDE_GREEN, self.entry.data.get(CONF_INCLUDE_GREEN, True)
        )
        include_sanitary = self.entry.options.get(
            CONF_INCLUDE_SANITARY, self.entry.data.get(CONF_INCLUDE_SANITARY, True)
        )
        tomorrow = today + timedelta(days=1)
        next_item = next_collection(
            today,
            zone,
            include_green,
            include_sanitary,
            include_start=True,
        )
        return {
            "today": today,
            "today_waste": collections_for_day(today, zone, include_green, include_sanitary),
            "tomorrow": tomorrow,
            "tomorrow_waste": collections_for_day(tomorrow, zone, include_green, include_sanitary),
            "next": next_item,
            "upcoming": list(upcoming_collections(today, zone, include_green, include_sanitary, 30)),
            "zone": zone,
        }
