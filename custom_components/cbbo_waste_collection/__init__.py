"""CBBO Waste Collection integration."""
from __future__ import annotations

from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS, SERVICE_CLEAR_CACHE, SERVICE_REFRESH
from .coordinator import CBBOWasteCoordinator
from .panel import async_setup_panel

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


def _loaded_coordinators(hass: HomeAssistant) -> list[CBBOWasteCoordinator]:
    """Return coordinators for loaded CBBO config entries."""
    coordinators: list[CBBOWasteCoordinator] = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        coordinator = getattr(entry, "runtime_data", None)
        if isinstance(coordinator, CBBOWasteCoordinator):
            coordinators.append(coordinator)
    return coordinators


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration-wide services and the sidebar panel."""
    await async_setup_panel(hass)

    async def refresh(_: ServiceCall) -> None:
        for coordinator in _loaded_coordinators(hass):
            await coordinator.async_request_refresh()

    async def clear_cache(_: ServiceCall) -> None:
        for coordinator in _loaded_coordinators(hass):
            await coordinator.async_clear_cache()
            await coordinator.async_request_refresh()

    _register_service_once(hass, SERVICE_REFRESH, refresh)
    _register_service_once(hass, SERVICE_CLEAR_CACHE, clear_cache)
    return True


def _register_service_once(
    hass: HomeAssistant,
    service: str,
    handler: Callable[[ServiceCall], object],
) -> None:
    """Register a service only when it is not already available."""
    if not hass.services.has_service(DOMAIN, service):
        hass.services.async_register(DOMAIN, service, handler)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up one CBBO config entry."""
    coordinator = CBBOWasteCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload one CBBO config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload an entry after its options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate legacy config entries without changing their entity IDs."""
    if entry.version < 2:
        hass.config_entries.async_update_entry(entry, version=2)
    return True
