"""CBBO sensors."""
from homeassistant.components.sensor import SensorDeviceClass,SensorEntity
from .entity import CBBOWasteEntity
from .schedule import ICONS
async def async_setup_entry(hass,entry,async_add_entities):
    c=entry.runtime_data;async_add_entities([Today(c),Tomorrow(c),Next(c),Days(c),LastUpdate(c),Source(c)])
def display(x):return " + ".join(x.labels) if x else "Nessun ritiro"
class CollectionSensor(CBBOWasteEntity,SensorEntity):
    key=""
    @property
    def native_value(self):return display(self.coordinator.data[self.key])
    @property
    def extra_state_attributes(self):
        x=self.coordinator.data[self.key];return {"waste_types":list(x.waste_types) if x else [],"waste_labels":list(x.labels) if x else [],"icons":[ICONS.get(i,"mdi:recycle") for i in x.waste_types] if x else [],"municipality":self.coordinator.data["municipality_name"],"zone":self.coordinator.data["zone"],"source":self.coordinator.data["source"],"data_source":self.coordinator.data["data_source"]}
class Today(CollectionSensor):
    _attr_translation_key="today";key="today_collection"
    def __init__(self,c):super().__init__(c,"today")
class Tomorrow(CollectionSensor):
    _attr_translation_key="tomorrow";key="tomorrow_collection"
    def __init__(self,c):super().__init__(c,"tomorrow")
class Next(CBBOWasteEntity,SensorEntity):
    _attr_translation_key="next_collection"
    def __init__(self,c):super().__init__(c,"next_collection")
    @property
    def native_value(self):return display(self.coordinator.data["next"])
    @property
    def extra_state_attributes(self):
        x=self.coordinator.data["next"];return {"date":x.day.isoformat() if x else None,"waste_types":list(x.waste_types) if x else [],"waste_labels":list(x.labels) if x else [],"data_source":self.coordinator.data["data_source"]}
class Days(CBBOWasteEntity,SensorEntity):
    _attr_translation_key="days_to_next";_attr_native_unit_of_measurement="d";_attr_icon="mdi:calendar-clock"
    def __init__(self,c):super().__init__(c,"days_to_next")
    @property
    def native_value(self):
        x=self.coordinator.data["next"];return (x.day-self.coordinator.data["today"]).days if x else None
class LastUpdate(CBBOWasteEntity,SensorEntity):
    _attr_translation_key="last_update";_attr_device_class=SensorDeviceClass.TIMESTAMP
    def __init__(self,c):super().__init__(c,"last_update")
    @property
    def native_value(self):return self.coordinator.data["last_update"]
class Source(CBBOWasteEntity,SensorEntity):
    _attr_translation_key="data_source";_attr_icon="mdi:database-sync"
    def __init__(self,c):super().__init__(c,"data_source")
    @property
    def native_value(self):return self.coordinator.data["data_source"]
    @property
    def extra_state_attributes(self):return {"source_url":self.coordinator.data["source"],"cache_used":self.coordinator.data["cache_used"],"last_error":self.coordinator.data["last_error"],"ecocalendar_pdf":self.coordinator.data.get("pdf_url")}
