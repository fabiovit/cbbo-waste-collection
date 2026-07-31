"""Coordinator for CBBO Waste Collection."""
from __future__ import annotations

import logging
from datetime import date, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import CBBOApiClient, CBBOApiError
from .const import (
    CACHE_VERSION,
    CONF_INCLUDE_GREEN,
    CONF_INCLUDE_SANITARY,
    CONF_MUNICIPALITY,
    CONF_ZONE,
    DEFAULT_SCAN_INTERVAL_HOURS,
    DOMAIN,
    MUNICIPALITIES,
    ZONE_DEFAULT,
)
from .schedule import Collection, GREEN, SANITARY

_LOGGER = logging.getLogger(__name__)


class CBBOWasteCoordinator(DataUpdateCoordinator[dict]):
    """Download and expose collection information shared by all entities."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.municipality = entry.data[CONF_MUNICIPALITY]
        self.zone = entry.data.get(CONF_ZONE, ZONE_DEFAULT)
        self.source_url = f"https://www.cbbo.it/{self.municipality}"
        self._api = CBBOApiClient(async_get_clientsession(hass))
        self._store: Store[dict] = Store(hass, CACHE_VERSION, f"{DOMAIN}.{entry.entry_id}")
        self._collections: list[Collection] = []
        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN}_{self.municipality}_{self.zone}",
            update_interval=timedelta(hours=DEFAULT_SCAN_INTERVAL_HOURS),
        )

    async def _async_update_data(self) -> dict:
        cache_used = False
        try:
            collections = await self._api.async_get_collections(self.municipality, self.zone)
            self._collections = collections
            await self._store.async_save({"collections": [self._serialize(x) for x in collections]})
        except CBBOApiError as err:
            cached = await self._store.async_load()
            if cached and cached.get("collections"):
                self._collections = [self._deserialize(item) for item in cached["collections"]]
                cache_used = True
                _LOGGER.warning("CBBO non raggiungibile; utilizzo la cache: %s", err)
            elif self._collections:
                cache_used = True
                _LOGGER.warning("CBBO non raggiungibile; mantengo i dati in memoria: %s", err)
            else:
                raise UpdateFailed(str(err)) from err

        return self._build_data(cache_used)

    def _build_data(self, cache_used: bool) -> dict:
        today = dt_util.now().date()
        tomorrow = today + timedelta(days=1)
        include_green = self.entry.options.get(
            CONF_INCLUDE_GREEN, self.entry.data.get(CONF_INCLUDE_GREEN, True)
        )
        include_sanitary = self.entry.options.get(
            CONF_INCLUDE_SANITARY, self.entry.data.get(CONF_INCLUDE_SANITARY, True)
        )
        filtered = [
            item for item in self._collections
            if include_green or GREEN not in item.waste_types
            if include_sanitary or SANITARY not in item.waste_types
        ]
        by_day = {item.day: item for item in filtered}
        upcoming = [item for item in filtered if today <= item.day <= today + timedelta(days=62)]
        next_item = next((item for item in filtered if item.day >= today), None)
        return {
            "today": today,
            "today_collection": by_day.get(today),
            "tomorrow": tomorrow,
            "tomorrow_collection": by_day.get(tomorrow),
            "next": next_item,
            "upcoming": upcoming,
            "municipality": self.municipality,
            "municipality_name": MUNICIPALITIES[self.municipality],
            "zone": self.zone,
            "source": self.source_url,
            "cache_used": cache_used,
        }

    @staticmethod
    def _serialize(item: Collection) -> dict:
        return {"day": item.day.isoformat(), "waste_types": list(item.waste_types), "labels": list(item.labels)}

    @staticmethod
    def _deserialize(item: dict) -> Collection:
        return Collection(date.fromisoformat(item["day"]), tuple(item["waste_types"]), tuple(item["labels"]))
