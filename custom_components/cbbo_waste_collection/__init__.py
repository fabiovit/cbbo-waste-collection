"""CBBO Waste Collection integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant,ServiceCall
from .const import DOMAIN,PLATFORMS,SERVICE_REFRESH,SERVICE_CLEAR_CACHE
from .coordinator import CBBOWasteCoordinator
from .panel import async_setup_panel

async def async_setup(hass:HomeAssistant,config:dict)->bool:
    await async_setup_panel(hass)
    async def refresh(call:ServiceCall):
        for entry in hass.config_entries.async_entries(DOMAIN):
            coordinator=getattr(entry,"runtime_data",None)
            if coordinator:await coordinator.async_request_refresh()
    async def clear_cache(call:ServiceCall):
        for entry in hass.config_entries.async_entries(DOMAIN):
            coordinator=getattr(entry,"runtime_data",None)
            if coordinator:
                await coordinator.async_clear_cache(); await coordinator.async_request_refresh()
    hass.services.async_register(DOMAIN,SERVICE_REFRESH,refresh)
    hass.services.async_register(DOMAIN,SERVICE_CLEAR_CACHE,clear_cache)
    return True

async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
    coordinator=CBBOWasteCoordinator(hass,entry); await coordinator.async_config_entry_first_refresh(); entry.runtime_data=coordinator
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS); entry.async_on_unload(entry.add_update_listener(_reload)); return True
async def async_unload_entry(hass,entry):return await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
async def _reload(hass,entry):await hass.config_entries.async_reload(entry.entry_id)
async def async_migrate_entry(hass,entry):
    if entry.version<2:
        hass.config_entries.async_update_entry(entry,version=2)
    return True
