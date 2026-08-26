"""Binary sensors for CBBO Waste Collection."""
from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CBBOWasteCoordinator
from .entity import CBBOWasteEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CBBO binary sensors."""
    coordinator: CBBOWasteCoordinator = entry.runtime_data
    async_add_entities(
        [
            CollectionTomorrowBinarySensor(coordinator),
            PutOutTonightBinarySensor(coordinator),
        ]
    )


class _TomorrowCollectionBase(CBBOWasteEntity, BinarySensorEntity):
    """Shared logic for binary sensors based on tomorrow's collection."""

    @property
    def _tomorrow(self):
        return self.coordinator.data["tomorrow_collection"]

    @property
    def is_on(self) -> bool:
        return self._tomorrow is not None

    def _collection_attributes(self) -> dict[str, Any]:
        collection = self._tomorrow
        return {
            "waste_labels": list(collection.labels) if collection else [],
            "waste_types": list(collection.waste_types) if collection else [],
            "source": self.coordinator.data["source"],
        }


class CollectionTomorrowBinarySensor(_TomorrowCollectionBase):
    """Whether a collection is scheduled tomorrow."""

    _attr_translation_key = "collection_tomorrow"
    _attr_icon = "mdi:truck-delivery"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "collection_tomorrow")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._collection_attributes()


class PutOutTonightBinarySensor(_TomorrowCollectionBase):
    """Whether waste should be put out tonight."""

    _attr_translation_key = "put_out_tonight"
    _attr_icon = "mdi:delete-clock"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "put_out_tonight")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            **self._collection_attributes(),
            "exposure_from": "22:00",
            "collection_by": "05:00",
        }
