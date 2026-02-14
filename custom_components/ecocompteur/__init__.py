"""Support for Legrand Ecocompteur."""

import ipaddress
import logging
import uuid
from dataclasses import dataclass

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

type EcocompteurConfigEntry = ConfigEntry[EcocompteurRuntimeData]


CONFIG_SCHEMA = vol.Schema(
    vol.All(
        cv.deprecated(DOMAIN),
        {
            DOMAIN: vol.Schema(
                {
                    vol.Required(CONF_HOST): vol.All(ipaddress.ip_address, cv.string),
                    vol.Optional(CONF_NAME): cv.string,
                }
            )
        },
    ),
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS: list[str] = [
    Platform.SENSOR,
]


@dataclass
class EcocompteurRuntimeData:
    """Ecocompteur runtime data."""

    name: str
    host: str


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old config entry to new format."""
    _LOGGER.debug("Migrating config entry from version %s", entry.version)

    if entry.version == 1:
        # Version 1 used a single unique ID for the entire integration
        # Version 2 uses a UUID per device to support multiple instances
        new_unique_id = str(uuid.uuid4())

        hass.config_entries.async_update_entry(
            entry,
            unique_id=new_unique_id,
            version=2,
        )

        _LOGGER.info(
            "Migrated config entry to version 2 with new unique ID: %s",
            new_unique_id,
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ecocompteur via a config entry."""
    host = entry.data[CONF_HOST]
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)
    entry.runtime_data = EcocompteurRuntimeData(name=name, host=host)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
