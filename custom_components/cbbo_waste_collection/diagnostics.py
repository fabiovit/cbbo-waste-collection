"""Diagnostics support for CBBO Waste Collection."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import CBBOWasteCoordinator

_TO_REDACT: set[str] = set()


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for one CBBO config entry."""
    coordinator: CBBOWasteCoordinator = entry.runtime_data
    data = coordinator.data or {}
    next_collection = data.get("next")

    return async_redact_data(
        {
            "entry": {
                "title": entry.title,
                "version": entry.version,
                "data": dict(entry.data),
                "options": dict(entry.options),
            },
            "coordinator": {
                "municipality": coordinator.municipality,
                "zone": coordinator.zone,
                "source_url": coordinator.source_url,
                "last_update": data.get("last_update"),
                "data_source": data.get("data_source"),
                "cache_used": data.get("cache_used"),
                "last_error": data.get("last_error"),
                "ecocalendar_pdf": data.get("pdf_url"),
                "collection_count": len(data.get("collections", [])),
                "next": next_collection.day.isoformat() if next_collection else None,
            },
        },
        _TO_REDACT,
    )
