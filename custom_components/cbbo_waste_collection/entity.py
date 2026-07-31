"""Base entity for CBBO Waste Collection."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MUNICIPALITY_ZONES, ZONE_DEFAULT


class CBBOWasteEntity(CoordinatorEntity):
    """Base coordinator entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entity_key: str) -> None:
        super().__init__(coordinator)
        municipality = coordinator.municipality
        zone = coordinator.zone
        suffix = municipality if zone == ZONE_DEFAULT else f"{municipality}_{zone}"
        self._attr_unique_id = f"{suffix}_{entity_key}"
        municipality_name = coordinator.data.get("municipality_name", municipality.title()) if coordinator.data else municipality.title()
        zone_name = MUNICIPALITY_ZONES.get(municipality, {}).get(zone)
        device_name = f"Differenziata {municipality_name}"
        if zone_name:
            device_name += f" - {zone_name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, suffix)},
            name=device_name,
            manufacturer="CBBO",
            model="Calendario raccolta online",
            configuration_url=coordinator.source_url,
        )
