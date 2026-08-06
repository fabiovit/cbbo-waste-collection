"""CBBO binary sensors."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from .entity import CBBOWasteEntity
async def async_setup_entry(hass,entry,async_add_entities):
    c=entry.runtime_data;async_add_entities([Tomorrow(c),Tonight(c)])
class Tomorrow(CBBOWasteEntity,BinarySensorEntity):
    _attr_translation_key="collection_tomorrow";_attr_icon="mdi:truck-delivery"
    def __init__(self,c):super().__init__(c,"collection_tomorrow")
    @property
    def is_on(self):return self.coordinator.data["tomorrow_collection"] is not None
    @property
    def extra_state_attributes(self):
        x=self.coordinator.data["tomorrow_collection"];return {"waste_labels":list(x.labels) if x else [],"waste_types":list(x.waste_types) if x else [],"source":self.coordinator.data["source"]}
class Tonight(CBBOWasteEntity,BinarySensorEntity):
    _attr_translation_key="put_out_tonight";_attr_icon="mdi:delete-clock"
    def __init__(self,c):super().__init__(c,"put_out_tonight")
    @property
    def is_on(self):return self.coordinator.data["tomorrow_collection"] is not None
    @property
    def extra_state_attributes(self):
        x=self.coordinator.data["tomorrow_collection"];return {"waste_labels":list(x.labels) if x else [],"waste_types":list(x.waste_types) if x else [],"exposure_from":"22:00","collection_by":"05:00","source":self.coordinator.data["source"]}
