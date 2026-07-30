"""Calendar entity for CBBO Waste Collection."""
from __future__ import annotations

from datetime import datetime, time, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .entity import CBBOWasteEntity
from .schedule import LABELS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([CBBOCalendar(entry.runtime_data)])


class CBBOCalendar(CBBOWasteEntity, CalendarEntity):
    _attr_translation_key = "calendar"
    _attr_icon = "mdi:recycle"
    def __init__(self, coordinator): super().__init__(coordinator, "calendar")

    @property
    def event(self):
        item = self.coordinator.data["next"]
        if not item:
            return None
        return self._event_from_collection(item)

    async def async_get_events(self, hass: HomeAssistant, start_date: datetime, end_date: datetime):
        events = []
        for item in self.coordinator.data["upcoming"]:
            start = dt_util.as_local(datetime.combine(item.day, time.min, tzinfo=dt_util.DEFAULT_TIME_ZONE))
            if start_date <= start < end_date:
                events.append(self._event_from_collection(item))
        return events

    @staticmethod
    def _event_from_collection(item):
        start = datetime.combine(item.day, time.min, tzinfo=dt_util.DEFAULT_TIME_ZONE)
        return CalendarEvent(
            start=start,
            end=start + timedelta(days=1),
            summary=" + ".join(LABELS[x] for x in item.waste_types),
            description="Esposizione dalla sera precedente alle 22:00 ed entro le 05:00.",
        )
