"""Base entity."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN,MUNICIPALITY_ZONES,ZONE_DEFAULT
class CBBOWasteEntity(CoordinatorEntity):
    _attr_has_entity_name=True
    def __init__(self,coordinator,key):
        super().__init__(coordinator); m=coordinator.municipality; z=coordinator.zone; suffix=m if z==ZONE_DEFAULT else f"{m}_{z}"; self._attr_unique_id=f"{suffix}_{key}"
        name=f"Differenziata {coordinator.data.get('municipality_name',m.title())}"; zn=MUNICIPALITY_ZONES.get(m,{}).get(z)
        if zn:name+=f" - {zn}"
        self._attr_device_info=DeviceInfo(identifiers={(DOMAIN,suffix)},name=name,manufacturer="CBBO",model="Calendario raccolta",configuration_url=coordinator.source_url)
