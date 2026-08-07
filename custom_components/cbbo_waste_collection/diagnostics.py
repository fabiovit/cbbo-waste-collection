"""Diagnostics support."""
from homeassistant.components.diagnostics import async_redact_data
TO_REDACT=set()
async def async_get_config_entry_diagnostics(hass,entry):
    c=entry.runtime_data; d=c.data or {}
    return async_redact_data({"entry":{"title":entry.title,"version":entry.version,"data":dict(entry.data),"options":dict(entry.options)},"coordinator":{"municipality":c.municipality,"zone":c.zone,"source_url":c.source_url,"last_update":d.get("last_update"),"data_source":d.get("data_source"),"cache_used":d.get("cache_used"),"last_error":d.get("last_error"),"ecocalendar_pdf":d.get("pdf_url"),"collection_count":len(d.get("collections",[])),"next":d.get("next").day.isoformat() if d.get("next") else None}},TO_REDACT)
