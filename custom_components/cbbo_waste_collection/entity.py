"""Base entity for CBBO Waste Collection."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SOURCE_URL


class CBBOWasteEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.unique_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.unique_id)},
            name=coordinator.entry.title,
            manufacturer="C.B.B.O. s.r.l.",
            model="Ecocalendario 2026",
            configuration_url=SOURCE_URL,
        )
