"""Frontend panel for CBBO Waste Collection."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.components import frontend, panel_custom, websocket_api
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN, MUNICIPALITY_ZONES, ZONE_DEFAULT

PANEL_COMPONENT = "cbbo-waste-collection-panel-v213"
PANEL_URL_PATH = "cbbo-waste-collection"
PANEL_JS_URL = "/cbbo_waste_collection/cbbo-panel.js"


def _iso(value: Any) -> Any:
    """Serialize dates and datetimes for the frontend."""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def _collection_payload(collection: Any) -> dict[str, Any] | None:
    """Serialize a collection object."""
    if collection is None:
        return None
    return {
        "date": _iso(collection.day),
        "waste_types": list(collection.waste_types),
        "labels": list(collection.labels),
    }


def _entry_payload(entry: Any) -> dict[str, Any] | None:
    """Serialize one loaded config entry."""
    coordinator = getattr(entry, "runtime_data", None)
    if coordinator is None or not getattr(coordinator, "data", None):
        return None

    data = coordinator.data
    municipality = coordinator.municipality
    zone = coordinator.zone
    zone_name = MUNICIPALITY_ZONES.get(municipality, {}).get(zone)
    if zone == ZONE_DEFAULT:
        zone_name = None

    today = data.get("today")
    next_collection = data.get("next")
    days_to_next = (
        (next_collection.day - today).days
        if next_collection is not None and today is not None
        else None
    )

    upcoming = []
    for collection in data.get("collections", []):
        if today is None or collection.day >= today:
            payload = _collection_payload(collection)
            if payload:
                upcoming.append(payload)
        if len(upcoming) >= 14:
            break

    return {
        "entry_id": entry.entry_id,
        "title": entry.title,
        "municipality": municipality,
        "municipality_name": data.get("municipality_name", municipality.title()),
        "zone": zone,
        "zone_name": zone_name,
        "today": _collection_payload(data.get("today_collection")),
        "tomorrow": _collection_payload(data.get("tomorrow_collection")),
        "next": _collection_payload(next_collection),
        "days_to_next": days_to_next,
        "put_out_tonight": data.get("tomorrow_collection") is not None,
        "collection_tomorrow": data.get("tomorrow_collection") is not None,
        "data_source": data.get("data_source"),
        "source_url": data.get("source"),
        "pdf_url": data.get("pdf_url"),
        "last_update": _iso(data.get("last_update")),
        "source_status": (
            "fallback"
            if str(data.get("data_source", "")).startswith("bundled_")
            else "cache"
            if data.get("cache_used", False)
            else "online"
        ),
        # A failed online parsing attempt is not an active error once a valid
        # cache or bundled calendar has successfully supplied the data.
        "last_error": (
            data.get("last_error")
            if not str(data.get("data_source", "")).startswith("bundled_")
            and not data.get("cache_used", False)
            else None
        ),
        "cache_used": data.get("cache_used", False),
        "upcoming": upcoming,
    }


@websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/panel_data"})
@callback
def websocket_panel_data(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return all loaded CBBO entries for the custom panel."""
    entries = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        payload = _entry_payload(entry)
        if payload is not None:
            entries.append(payload)

    connection.send_result(
        msg["id"],
        {
            "version": "2.1.3",
            "entries": entries,
            "ko_fi": "https://ko-fi.com/fabvittori",
        },
    )


async def async_setup_panel(hass: HomeAssistant) -> None:
    """Register the sidebar panel and its frontend resource."""
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                PANEL_JS_URL,
                str(Path(__file__).parent / "frontend" / "cbbo-panel.js"),
                False,
            )
        ]
    )

    websocket_api.async_register_command(hass, websocket_panel_data)

    if not frontend.async_panel_exists(hass, PANEL_URL_PATH):
        await panel_custom.async_register_panel(
            hass,
            frontend_url_path=PANEL_URL_PATH,
            webcomponent_name=PANEL_COMPONENT,
            sidebar_title="CBBO Waste Collection",
            sidebar_icon="mdi:recycle",
            module_url=f"{PANEL_JS_URL}?v=2.1.3",
            require_admin=False,
        )
