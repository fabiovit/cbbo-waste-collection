"""Config flow for CBBO Waste Collection."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

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


def _select(options: dict[str, str]) -> selector.SelectSelector:
    """Build a Home Assistant dropdown selector from a value/label mapping."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                selector.SelectOptionDict(value=value, label=label)
                for value, label in options.items()
            ],
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


class CBBOWasteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure a CBBO municipality and optional zone."""

    VERSION = 3

    def __init__(self) -> None:
        self._municipality: str | None = None

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            self._municipality = user_input[CONF_MUNICIPALITY]
            if self._municipality in MUNICIPALITY_ZONES:
                return await self.async_step_zone()
            return await self._create_entry(ZONE_DEFAULT)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_MUNICIPALITY): _select(MUNICIPALITIES)}
            ),
        )

    async def async_step_zone(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            return await self._create_entry(user_input[CONF_ZONE])

        assert self._municipality is not None
        return self.async_show_form(
            step_id="zone",
            data_schema=vol.Schema(
                {vol.Required(CONF_ZONE): _select(MUNICIPALITY_ZONES[self._municipality])}
            ),
        )

    async def _create_entry(self, zone: str) -> config_entries.ConfigFlowResult:
        assert self._municipality is not None

        unique_id = f"{self._municipality}:{zone}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        title = f"Differenziata {MUNICIPALITIES[self._municipality]}"
        zone_name = MUNICIPALITY_ZONES.get(self._municipality, {}).get(zone)
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

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return CBBOOptionsFlow(config_entry)


class CBBOOptionsFlow(config_entries.OptionsFlow):
    """Configure optional collection categories."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INCLUDE_GREEN,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_GREEN,
                            self.config_entry.data.get(CONF_INCLUDE_GREEN, True),
                        ),
                    ): bool,
                    vol.Required(
                        CONF_INCLUDE_SANITARY,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_SANITARY,
                            self.config_entry.data.get(CONF_INCLUDE_SANITARY, True),
                        ),
                    ): bool,
                }
            ),
        )
