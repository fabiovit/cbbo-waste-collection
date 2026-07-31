"""Binary sensors for CBBO Waste Collection."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import CBBOWasteEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = entry.runtime_data
    async_add_entities([CBBORitiroDomani(coordinator), CBBOEsporreStasera(coordinator)])


class CBBORitiroDomani(CBBOWasteEntity, BinarySensorEntity):
    _attr_translation_key = "collection_tomorrow"
    _attr_icon = "mdi:truck-delivery"
    def __init__(self, coordinator): super().__init__(coordinator, "collection_tomorrow")

    @property
    def is_on(self):
        return self.coordinator.data["tomorrow_collection"] is not None

    @property
    def extra_state_attributes(self):
        item = self.coordinator.data["tomorrow_collection"]
        return {"waste_labels": list(item.labels) if item else [], "source": self.coordinator.data["source"]}


class CBBOEsporreStasera(CBBOWasteEntity, BinarySensorEntity):
    _attr_translation_key = "put_out_tonight"
    _attr_icon = "mdi:delete-clock"
    def __init__(self, coordinator): super().__init__(coordinator, "put_out_tonight")

    @property
    def is_on(self):
        return self.coordinator.data["tomorrow_collection"] is not None

    @property
    def extra_state_attributes(self):
        item = self.coordinator.data["tomorrow_collection"]
        return {
            "waste_labels": list(item.labels) if item else [],
            "exposure_from": "22:00",
            "collection_by": "05:00",
            "source": self.coordinator.data["source"],
        }
