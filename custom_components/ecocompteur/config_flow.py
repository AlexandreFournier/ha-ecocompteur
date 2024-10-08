"""Config flow for Ecocompteur integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_NAME

from .api import Ecocompteur, EcocompteurApiError
from .const import DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,  # type: ignore  # noqa: PGH003
        vol.Required(CONF_HOST): str,
    }
)


class EcocompteurConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ecocompteur."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            client = Ecocompteur(self.hass, host)
            try:
                await client.fetch_data()
            except EcocompteurApiError:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"
            else:
                await self._async_handle_discovery_without_unique_id()
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
