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
    MUNICIPALITY_MAZZANO,
    ZONE_NORTH,
    ZONE_SOUTH,
)


class CBBOWasteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_MUNICIPALITY]}_{user_input[CONF_ZONE]}"
            )
            self._abort_if_unique_id_configured()
            title_zone = "Nord" if user_input[CONF_ZONE] == ZONE_NORTH else "Sud"
            return self.async_create_entry(
                title=f"Differenziata Mazzano - Zona {title_zone}", data=user_input
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_MUNICIPALITY, default=MUNICIPALITY_MAZZANO): vol.In(
                    {MUNICIPALITY_MAZZANO: "Mazzano"}
                ),
                vol.Required(CONF_ZONE): vol.In(
                    {ZONE_NORTH: "Zona Nord", ZONE_SOUTH: "Zona Sud"}
                ),
                vol.Optional(CONF_INCLUDE_GREEN, default=True): bool,
                vol.Optional(CONF_INCLUDE_SANITARY, default=True): bool,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

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
