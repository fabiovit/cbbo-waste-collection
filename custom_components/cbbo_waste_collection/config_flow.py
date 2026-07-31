"""Config flow for CBBO Waste Collection."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_INCLUDE_GREEN,
    CONF_INCLUDE_SANITARY,
    CONF_MUNICIPALITY,
    CONF_ZONE,
    DOMAIN,
    MUNICIPALITIES,
    MUNICIPALITY_ZONES,
    ZONE_DEFAULT,
)


class CBBOWasteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 2
    MINOR_VERSION = 0

    def __init__(self) -> None:
        self._municipality: str | None = None

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            self._municipality = user_input[CONF_MUNICIPALITY]
            if self._municipality in MUNICIPALITY_ZONES:
                return await self.async_step_zone()
            return await self._create_entry(ZONE_DEFAULT)

        schema = vol.Schema(
            {vol.Required(CONF_MUNICIPALITY): vol.In(MUNICIPALITIES)}
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_zone(self, user_input: dict[str, Any] | None = None):
        assert self._municipality is not None
        if user_input is not None:
            return await self._create_entry(user_input[CONF_ZONE])

        schema = vol.Schema(
            {vol.Required(CONF_ZONE): vol.In(MUNICIPALITY_ZONES[self._municipality])}
        )
        return self.async_show_form(step_id="zone", data_schema=schema)

    async def _create_entry(self, zone: str):
        assert self._municipality is not None
        unique_id = self._municipality if zone == ZONE_DEFAULT else f"{self._municipality}_{zone}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()
        municipality_name = MUNICIPALITIES[self._municipality]
        zone_name = MUNICIPALITY_ZONES.get(self._municipality, {}).get(zone)
        title = f"Differenziata {municipality_name}"
        if zone_name:
            title += f" - {zone_name}"
        return self.async_create_entry(
            title=title,
            data={
                CONF_MUNICIPALITY: self._municipality,
                CONF_ZONE: zone,
                CONF_INCLUDE_GREEN: True,
                CONF_INCLUDE_SANITARY: True,
            },
        )

    async def async_migrate_entry(self, hass, config_entry) -> bool:
        """Migrate the original Mazzano-only entry without changing entity IDs."""
        if config_entry.version == 1:
            data = {**config_entry.data}
            data.setdefault(CONF_MUNICIPALITY, "mazzano")
            data.setdefault(CONF_ZONE, ZONE_DEFAULT)
            hass.config_entries.async_update_entry(config_entry, data=data, version=2)
        return True

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CBBOWasteOptionsFlow()


class CBBOWasteOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_INCLUDE_GREEN,
                    default=self.config_entry.options.get(
                        CONF_INCLUDE_GREEN,
                        self.config_entry.data.get(CONF_INCLUDE_GREEN, True),
                    ),
                ): bool,
                vol.Optional(
                    CONF_INCLUDE_SANITARY,
                    default=self.config_entry.options.get(
                        CONF_INCLUDE_SANITARY,
                        self.config_entry.data.get(CONF_INCLUDE_SANITARY, True),
                    ),
                ): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
