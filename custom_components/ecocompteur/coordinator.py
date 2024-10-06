"""Coordinator for Ecocompteur ventilation units."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import Ecocompteur, EcocompteurApiError
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
        try:
            self.data = {
                "config": await self.client.fetch_data(),
                "values": await self.client.fetch_inst(),
            }
        except EcocompteurApiError as err:
            msg = "Error during state cache update"
            raise UpdateFailed(msg) from err

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch state update."""
        try:
            self.data = {
                "config": await self.client.fetch_data(),
                "values": await self.client.fetch_inst(),
            }
        except EcocompteurApiError as err:
            msg = "Error during state cache update"
            raise UpdateFailed(msg) from err
        else:
            return self.data
