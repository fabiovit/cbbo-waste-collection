"""Binary sensors for CBBO Waste Collection."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import CBBOWasteEntity
from .schedule import LABELS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = entry.runtime_data
    async_add_entities([CBBORetiroDomani(coordinator), CBBOEsporreStasera(coordinator)])


class CBBORetiroDomani(CBBOWasteEntity, BinarySensorEntity):
    _attr_translation_key = "collection_tomorrow"
    _attr_icon = "mdi:truck-delivery"
    def __init__(self, coordinator): super().__init__(coordinator, "collection_tomorrow")
    @property
    def is_on(self): return bool(self.coordinator.data["tomorrow_waste"])
    @property
    def extra_state_attributes(self):
        waste = self.coordinator.data["tomorrow_waste"]
        return {"waste_labels": [LABELS[x] for x in waste]}


class CBBOEsporreStasera(CBBOWasteEntity, BinarySensorEntity):
    _attr_translation_key = "put_out_tonight"
    _attr_icon = "mdi:delete-clock"
    def __init__(self, coordinator): super().__init__(coordinator, "put_out_tonight")
    @property
    def is_on(self):
        return bool(self.coordinator.data["tomorrow_waste"])
    @property
    def extra_state_attributes(self):
        waste = self.coordinator.data["tomorrow_waste"]
        return {
            "waste_labels": [LABELS[x] for x in waste],
            "exposure_from": "22:00",
            "collection_by": "05:00",
        }
