"""CBBO collection calendar."""
from datetime import datetime,time,timedelta
from homeassistant.components.calendar import CalendarEntity,CalendarEvent
from homeassistant.util import dt as dt_util
from .entity import CBBOWasteEntity
async def async_setup_entry(hass,entry,async_add_entities):async_add_entities([CBBOCalendar(entry.runtime_data)])
class CBBOCalendar(CBBOWasteEntity,CalendarEntity):
    _attr_translation_key="calendar";_attr_icon="mdi:recycle"
    def __init__(self,c):super().__init__(c,"calendar")
    @property
    def event(self):
        x=self.coordinator.data["next"];return self._to_event(x) if x else None
    async def async_get_events(self,hass,start_date,end_date):
        result=[]
        for x in self.coordinator.data["collections"]:
            start=datetime.combine(x.day,time.min,tzinfo=dt_util.DEFAULT_TIME_ZONE)
            if start_date<=start<end_date:result.append(self._to_event(x))
        return result
    @staticmethod
    def _to_event(x):
        start=datetime.combine(x.day,time.min,tzinfo=dt_util.DEFAULT_TIME_ZONE)
        return CalendarEvent(start=start,end=start+timedelta(days=1),summary=" + ".join(x.labels),description="Esposizione dalla sera precedente alle 22:00 ed entro le 05:00.")
