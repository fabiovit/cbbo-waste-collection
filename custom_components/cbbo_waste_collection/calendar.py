"""Calendar platform for CBBO Waste Collection."""
from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CBBOWasteCoordinator
from .entity import CBBOWasteEntity
from .schedule import Collection

_EVENT_DESCRIPTION = (
    "Esposizione dalla sera precedente alle 22:00 ed entro le 05:00."
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CBBO collection calendar."""
    async_add_entities([CBBOCalendar(entry.runtime_data)])


class CBBOCalendar(CBBOWasteEntity, CalendarEntity):
    """Calendar containing all known CBBO collection events."""

    _attr_translation_key = "calendar"
    _attr_icon = "mdi:recycle"

    def __init__(self, coordinator: CBBOWasteCoordinator) -> None:
        super().__init__(coordinator, "calendar")

    @property
    def event(self) -> CalendarEvent | None:
        collection = self.coordinator.data["next"]
        return self._to_event(collection) if collection else None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return collection events in the requested date range."""
        start = start_date.date()
        end = end_date.date()
        return [
            self._to_event(collection)
            for collection in self.coordinator.data["collections"]
            if start <= collection.day < end
        ]

    @staticmethod
    def _to_event(collection: Collection) -> CalendarEvent:
        return CalendarEvent(
            start=collection.day,
            end=collection.day + timedelta(days=1),
            summary=" + ".join(collection.labels),
            description=_EVENT_DESCRIPTION,
        )
