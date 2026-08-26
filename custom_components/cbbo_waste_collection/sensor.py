"""Sensors for CBBO Waste Collection."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CBBOWasteCoordinator
from .entity import CBBOWasteEntity
from .schedule import Collection, ICONS

_NO_COLLECTION = "Nessun ritiro"


def _display(collection: Collection | None) -> str:
    return " + ".join(collection.labels) if collection else _NO_COLLECTION


def _collection_attributes(collection: Collection | None) -> dict[str, Any]:
    if collection is None:
        return {"waste_types": [], "waste_labels": [], "icons": []}

    return {
        "waste_types": list(collection.waste_types),
        "waste_labels": list(collection.labels),
        "icons": [ICONS.get(item, "mdi:recycle") for item in collection.waste_types],
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CBBO sensors."""
    coordinator: CBBOWasteCoordinator = entry.runtime_data
    async_add_entities(
        [
            TodaySensor(coordinator),
            TomorrowSensor(coordinator),
            NextCollectionSensor(coordinator),
            DaysToNextSensor(coordinator),
            LastUpdateSensor(coordinator),
            DataSourceSensor(coordinator),
        ]
    )


class CollectionSensor(CBBOWasteEntity, SensorEntity):
    """Base sensor for a collection field in coordinator data."""

    coordinator_key = ""

    @property
    def native_value(self) -> str:
        return _display(self.coordinator.data[self.coordinator_key])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        collection = self.coordinator.data[self.coordinator_key]
        return {
            **_collection_attributes(collection),
            "municipality": self.coordinator.data["municipality_name"],
            "zone": self.coordinator.data["zone"],
            "source": self.coordinator.data["source"],
            "data_source": self.coordinator.data["data_source"],
        }


class TodaySensor(CollectionSensor):
    _attr_translation_key = "today"
    coordinator_key = "today_collection"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "today")


class TomorrowSensor(CollectionSensor):
    _attr_translation_key = "tomorrow"
    coordinator_key = "tomorrow_collection"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "tomorrow")


class NextCollectionSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "next_collection"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "next_collection")

    @property
    def native_value(self) -> str:
        return _display(self.coordinator.data["next"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        collection = self.coordinator.data["next"]
        return {
            "date": collection.day.isoformat() if collection else None,
            **_collection_attributes(collection),
            "data_source": self.coordinator.data["data_source"],
        }


class DaysToNextSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "days_to_next"
    _attr_native_unit_of_measurement = "d"
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "days_to_next")

    @property
    def native_value(self) -> int | None:
        collection = self.coordinator.data["next"]
        if collection is None:
            return None
        return (collection.day - self.coordinator.data["today"]).days


class LastUpdateSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "last_update"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "last_update")

    @property
    def native_value(self):
        return self.coordinator.data["last_update"]


class DataSourceSensor(CBBOWasteEntity, SensorEntity):
    _attr_translation_key = "data_source"
    _attr_icon = "mdi:database-sync"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "data_source")

    @property
    def native_value(self) -> str:
        return self.coordinator.data["data_source"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "source_url": self.coordinator.data["source"],
            "cache_used": self.coordinator.data["cache_used"],
            "last_error": self.coordinator.data["last_error"],
            "ecocalendar_pdf": self.coordinator.data.get("pdf_url"),
        }
