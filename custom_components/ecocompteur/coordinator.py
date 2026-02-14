"""Coordinator for Ecocompteur ventilation units."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import Ecocompteur, EcocompteurApiError, EcocompteurJSONDecodeError
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class EcocompteurDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """The DataUpdateCoordinator for Ecocompteur."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        client: Ecocompteur,
    ) -> None:
        """Initialize Ecocompteur data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{name} DataUpdateCoordinator",
            update_interval=DEFAULT_SCAN_INTERVAL,
            always_update=False,
        )
        self.client = client

    async def _async_setup(self) -> None:
        """Set up the coordinator."""
        self.data = await self._async_update_data()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch state update."""
        try:
            return {
                "config": await self.client.fetch_data(),
                "values": await self.client.fetch_inst(),
            }
        except EcocompteurApiError as err:
            msg = "Error communicating with Ecocompteur"
            raise UpdateFailed(msg) from err
        except EcocompteurJSONDecodeError as err:
            msg = "Error decoding Ecocompteur JSON response"
            raise UpdateFailed(msg) from err
