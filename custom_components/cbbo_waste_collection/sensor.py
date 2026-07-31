"""Sensors for CBBO Waste Collection."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import CBBOWasteEntity
from .schedule import ICONS


def _display(item) -> str:
    return " + ".join(item.labels) if item else "Nessun ritiro"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = entry.runtime_data
    async_add_entities([
        CBBOTodaySensor(coordinator),
        CBBOTomorrowSensor(coordinator),
        CBBONextSensor(coordinator),
        CBBODaysToNextSensor(coordinator),
    ])


class _CollectionSensor(CBBOWasteEntity, SensorEntity):
    data_key: str

    @property
    def native_value(self):
        return _display(self.coordinator.data[self.data_key])

    @property
    def extra_state_attributes(self):
        item = self.coordinator.data[self.data_key]
        return {
            "waste_types": list(item.waste_types) if item else [],
            "waste_labels": list(item.labels) if item else [],
            "icons": [ICONS.get(x, "mdi:recycle") for x in item.waste_types] if item else [],
            "municipality": self.coordinator.data["municipality_name"],
            "zone": self.coordinator.data["zone"],
            "source": self.coordinator.data["source"],
            "cache_used": self.coordinator.data["cache_used"],
            "data_source": self.coordinator.data["data_source"],
        }


class CBBOTodaySensor(_CollectionSensor):
    _attr_translation_key = "today"
    data_key = "today_collection"
    def __init__(self, coordinator): super().__init__(coordinator, "today")


class CBBOTomorrowSensor(_CollectionSensor):
    _attr_translation_key = "tomorrow"
    data_key = "tomorrow_collection"
    def __init__(self, coordinator): super().__init__(coordinator, "tomorrow")


class CBBONextSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "next_collection"
    def __init__(self, coordinator): super().__init__(coordinator, "next_collection")

    @property
    def native_value(self):
        return _display(self.coordinator.data["next"])

    @property
    def extra_state_attributes(self):
        item = self.coordinator.data["next"]
        return {
            "date": item.day.isoformat() if item else None,
            "waste_types": list(item.waste_types) if item else [],
            "waste_labels": list(item.labels) if item else [],
            "municipality": self.coordinator.data["municipality_name"],
            "zone": self.coordinator.data["zone"],
            "source": self.coordinator.data["source"],
            "cache_used": self.coordinator.data["cache_used"],
            "data_source": self.coordinator.data["data_source"],
        }


class CBBODaysToNextSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "days_to_next"
    _attr_native_unit_of_measurement = "d"
    _attr_icon = "mdi:calendar-clock"
    def __init__(self, coordinator): super().__init__(coordinator, "days_to_next")

    @property
    def native_value(self):
        item = self.coordinator.data["next"]
        return (item.day - self.coordinator.data["today"]).days if item else None
