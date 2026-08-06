"""Config flow for CBBO Waste Collection."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import *

class CBBOWasteConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
    VERSION=2
    def __init__(self):self._municipality=None
    async def async_step_user(self,user_input=None):
        if user_input:
            self._municipality=user_input[CONF_MUNICIPALITY]
            if self._municipality in MUNICIPALITY_ZONES:return await self.async_step_zone()
            return await self._create(ZONE_DEFAULT)
        schema=vol.Schema({vol.Required(CONF_MUNICIPALITY):selector.SelectSelector(selector.SelectSelectorConfig(options=[selector.SelectOptionDict(value=k,label=v) for k,v in MUNICIPALITIES.items()],mode=selector.SelectSelectorMode.DROPDOWN))})
        return self.async_show_form(step_id="user",data_schema=schema)
    async def async_step_zone(self,user_input=None):
        if user_input:return await self._create(user_input[CONF_ZONE])
        zones=MUNICIPALITY_ZONES[self._municipality]
        schema=vol.Schema({vol.Required(CONF_ZONE):selector.SelectSelector(selector.SelectSelectorConfig(options=[selector.SelectOptionDict(value=k,label=v) for k,v in zones.items()],mode=selector.SelectSelectorMode.DROPDOWN))})
        return self.async_show_form(step_id="zone",data_schema=schema)
    async def _create(self,zone):
        unique=f"{self._municipality}:{zone}"; await self.async_set_unique_id(unique); self._abort_if_unique_id_configured()
        name=f"Differenziata {MUNICIPALITIES[self._municipality]}"; z=MUNICIPALITY_ZONES.get(self._municipality,{}).get(zone)
        if z:name+=f" - {z}"
        return self.async_create_entry(title=name,data={CONF_MUNICIPALITY:self._municipality,CONF_ZONE:zone,CONF_INCLUDE_GREEN:True,CONF_INCLUDE_SANITARY:True})
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):return OptionsFlow(config_entry)
class OptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self,user_input=None):
        if user_input:return self.async_create_entry(title="",data=user_input)
        schema=vol.Schema({vol.Required(CONF_INCLUDE_GREEN,default=self.config_entry.options.get(CONF_INCLUDE_GREEN,self.config_entry.data.get(CONF_INCLUDE_GREEN,True))):bool,vol.Required(CONF_INCLUDE_SANITARY,default=self.config_entry.options.get(CONF_INCLUDE_SANITARY,self.config_entry.data.get(CONF_INCLUDE_SANITARY,True))):bool})
        return self.async_show_form(step_id="init",data_schema=schema)
