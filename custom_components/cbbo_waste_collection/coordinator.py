"""Data coordinator for CBBO Waste Collection."""
from __future__ import annotations
import logging
from datetime import date,timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator,UpdateFailed
from homeassistant.util import dt as dt_util
from .api import CBBOApiClient,CBBOApiError
from .const import *
from .schedule import Collection,GREEN,SANITARY
from .bundled_2026 import build as build_bundled_2026
_LOGGER=logging.getLogger(__name__)

class CBBOWasteCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self,hass:HomeAssistant,entry:ConfigEntry):
        self.entry=entry; self.municipality=entry.data[CONF_MUNICIPALITY]; self.zone=entry.data.get(CONF_ZONE,ZONE_DEFAULT)
        self.source_url=f"{BASE_URL}/{self.municipality}"; self._api=CBBOApiClient(async_get_clientsession(hass))
        self._store:Store[dict]=Store(hass,CACHE_VERSION,f"{DOMAIN}.{entry.entry_id}"); self._collections=[]; self.last_error=None; self.pdf_url=None
        super().__init__(hass,logger=_LOGGER,name=f"{DOMAIN}_{self.municipality}_{self.zone}",update_interval=UPDATE_INTERVAL)
    async def _async_update_data(self):
        cache_used=False; source="online"; self.last_error=None
        try:
            self._collections=await self._api.async_get_collections(self.municipality,self.zone); self.pdf_url=self._api.last_pdf_url
            await self._store.async_save({"saved_at":dt_util.utcnow().isoformat(),"collections":[self._serialize(x) for x in self._collections]})
        except CBBOApiError as err:
            self.pdf_url=self._api.last_pdf_url; self.last_error=str(err); cached=await self._store.async_load()
            if cached and cached.get("collections"):
                self._collections=[self._deserialize(x) for x in cached["collections"]]; cache_used=True; source="cache"
            elif self._collections:cache_used=True;source="memory"
            else:
                bundled=build_bundled_2026(self.municipality,self.zone)
                if bundled:
                    self._collections=bundled;source=f"bundled_{self.municipality.replace('-', '_')}_2026"
                else:
                    raise UpdateFailed(str(err)) from err
            _LOGGER.warning("CBBO update fallback %s: %s",source,err)
        return self._build(cache_used,source)
    def _build(self,cache_used,source):
        today=dt_util.now().date(); include_green=self.entry.options.get(CONF_INCLUDE_GREEN,self.entry.data.get(CONF_INCLUDE_GREEN,True)); include_sanitary=self.entry.options.get(CONF_INCLUDE_SANITARY,self.entry.data.get(CONF_INCLUDE_SANITARY,True))
        filtered=[x for x in self._collections if (include_green or GREEN not in x.waste_types) and (include_sanitary or SANITARY not in x.waste_types)]
        by_day={x.day:x for x in filtered}; next_item=next((x for x in filtered if x.day>=today),None)
        return {"today":today,"today_collection":by_day.get(today),"tomorrow_collection":by_day.get(today+timedelta(days=1)),"next":next_item,"collections":filtered,"municipality":self.municipality,"municipality_name":MUNICIPALITIES[self.municipality],"zone":self.zone,"source":self.source_url,"cache_used":cache_used,"data_source":source,"last_update":dt_util.utcnow(),"last_error":self.last_error,"pdf_url":self.pdf_url}
    async def async_clear_cache(self):
        await self._store.async_remove(); self._collections=[]
    @staticmethod
    def _serialize(x):return {"day":x.day.isoformat(),"waste_types":list(x.waste_types),"labels":list(x.labels)}
    @staticmethod
    def _deserialize(x):return Collection(date.fromisoformat(x["day"]),tuple(x["waste_types"]),tuple(x["labels"]))
