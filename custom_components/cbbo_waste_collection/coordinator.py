"""Data coordinator for CBBO Waste Collection."""
from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import CBBOApiClient, CBBOApiError
from .bundled_2026 import build as build_bundled_2026
from .const import (
    BASE_URL,
    CACHE_VERSION,
    CONF_INCLUDE_GREEN,
    CONF_INCLUDE_SANITARY,
    CONF_MUNICIPALITY,
    CONF_ZONE,
    DOMAIN,
    MUNICIPALITIES,
    UPDATE_INTERVAL,
    ZONE_DEFAULT,
)
from .schedule import Collection, GREEN, SANITARY

_LOGGER = logging.getLogger(__name__)


class CBBOWasteCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch, cache and expose collection data for one municipality/zone."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.municipality = entry.data[CONF_MUNICIPALITY]
        self.zone = entry.data.get(CONF_ZONE, ZONE_DEFAULT)
        self.source_url = f"{BASE_URL}/{self.municipality}"

        self._api = CBBOApiClient(async_get_clientsession(hass))
        self._store: Store[dict[str, Any]] = Store(
            hass,
            CACHE_VERSION,
            f"{DOMAIN}.{entry.entry_id}",
        )
        self._collections: list[Collection] = []

        self.last_error: str | None = None
        self.pdf_url: str | None = None

        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN}_{self.municipality}_{self.zone}",
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update from CBBO and transparently fall back when necessary."""
        cache_used = False
        data_source = "online"
        self.last_error = None

        try:
            self._collections = await self._api.async_get_collections(
                self.municipality,
                self.zone,
            )
            self.pdf_url = self._api.last_pdf_url
            await self._save_cache()
        except CBBOApiError as err:
            self.pdf_url = self._api.last_pdf_url
            self.last_error = str(err)
            cache_used, data_source = await self._load_fallback(err)

        return self._build_data(cache_used=cache_used, data_source=data_source)

    async def _save_cache(self) -> None:
        """Persist the latest valid collection calendar."""
        await self._store.async_save(
            {
                "saved_at": dt_util.utcnow().isoformat(),
                "collections": [self._serialize(item) for item in self._collections],
            }
        )

    async def _load_fallback(self, err: CBBOApiError) -> tuple[bool, str]:
        """Load cache, memory or bundled data after an online failure."""
        cached = await self._store.async_load()

        if cached and cached.get("collections"):
            self._collections = [
                self._deserialize(item) for item in cached["collections"]
            ]
            source = "cache"
            cache_used = True
        elif self._collections:
            source = "memory"
            cache_used = True
        else:
            bundled = build_bundled_2026(self.municipality, self.zone)
            if not bundled:
                raise UpdateFailed(str(err)) from err
            self._collections = bundled
            source = f"bundled_{self.municipality.replace('-', '_')}_2026"
            cache_used = False

        _LOGGER.warning("CBBO update fallback %s: %s", source, err)
        return cache_used, source

    def _build_data(self, *, cache_used: bool, data_source: str) -> dict[str, Any]:
        """Build the coordinator payload consumed by entities and the panel."""
        today = dt_util.now().date()
        filtered = self._filtered_collections()
        by_day = {item.day: item for item in filtered}
        next_item = next((item for item in filtered if item.day >= today), None)

        return {
            "today": today,
            "today_collection": by_day.get(today),
            "tomorrow_collection": by_day.get(today + timedelta(days=1)),
            "next": next_item,
            "collections": filtered,
            "municipality": self.municipality,
            "municipality_name": MUNICIPALITIES[self.municipality],
            "zone": self.zone,
            "source": self.source_url,
            "cache_used": cache_used,
            "data_source": data_source,
            "last_update": dt_util.utcnow(),
            "last_error": self.last_error,
            "pdf_url": self.pdf_url,
        }

    def _filtered_collections(self) -> list[Collection]:
        """Apply user options without mutating the source collection list."""
        include_green = self.entry.options.get(
            CONF_INCLUDE_GREEN,
            self.entry.data.get(CONF_INCLUDE_GREEN, True),
        )
        include_sanitary = self.entry.options.get(
            CONF_INCLUDE_SANITARY,
            self.entry.data.get(CONF_INCLUDE_SANITARY, True),
        )

        return [
            item
            for item in self._collections
            if (include_green or GREEN not in item.waste_types)
            and (include_sanitary or SANITARY not in item.waste_types)
        ]

    async def async_clear_cache(self) -> None:
        """Clear persistent and in-memory collection data."""
        await self._store.async_remove()
        self._collections = []

    @staticmethod
    def _serialize(item: Collection) -> dict[str, Any]:
        return {
            "day": item.day.isoformat(),
            "waste_types": list(item.waste_types),
            "labels": list(item.labels),
        }

    @staticmethod
    def _deserialize(item: dict[str, Any]) -> Collection:
        return Collection(
            date.fromisoformat(item["day"]),
            tuple(item["waste_types"]),
            tuple(item["labels"]),
        )
