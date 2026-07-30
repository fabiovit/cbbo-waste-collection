"""Sensors for CBBO Waste Collection."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CALENDAR_URL_2026
from .entity import CBBOWasteEntity
from .schedule import ICONS, LABELS


def _display(waste: tuple[str, ...]) -> str:
    return " + ".join(LABELS[item] for item in waste) if waste else "Nessun ritiro"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        [
            CBBOTodaySensor(coordinator),
            CBBOTomorrowSensor(coordinator),
            CBBONextSensor(coordinator),
            CBBODaysToNextSensor(coordinator),
        ]
    )


class _CollectionSensor(CBBOWasteEntity, SensorEntity):
    data_key: str

    @property
    def native_value(self):
        return _display(self.coordinator.data[self.data_key])

    @property
    def extra_state_attributes(self):
        waste = self.coordinator.data[self.data_key]
        return {
            "waste_types": list(waste),
            "waste_labels": [LABELS[item] for item in waste],
            "icons": [ICONS[item] for item in waste],
            "zone": self.coordinator.data["zone"],
            "source": CALENDAR_URL_2026,
        }


class CBBOTodaySensor(_CollectionSensor):
    _attr_translation_key = "today"
    data_key = "today_waste"
    def __init__(self, coordinator): super().__init__(coordinator, "today")


class CBBOTomorrowSensor(_CollectionSensor):
    _attr_translation_key = "tomorrow"
    data_key = "tomorrow_waste"
    def __init__(self, coordinator): super().__init__(coordinator, "tomorrow")


class CBBONextSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "next_collection"
    def __init__(self, coordinator): super().__init__(coordinator, "next_collection")
    @property
    def native_value(self):
        item = self.coordinator.data["next"]
        return _display(item.waste_types) if item else "Nessun ritiro"
    @property
    def extra_state_attributes(self):
        item = self.coordinator.data["next"]
        return {
            "date": item.day.isoformat() if item else None,
            "waste_types": list(item.waste_types) if item else [],
            "waste_labels": [LABELS[x] for x in item.waste_types] if item else [],
            "zone": self.coordinator.data["zone"],
            "source": CALENDAR_URL_2026,
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
