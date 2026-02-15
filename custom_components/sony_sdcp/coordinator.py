"""DataUpdateCoordinator for Sony SDCP."""

from __future__ import annotations

from datetime import timedelta
import logging

import pysdcp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_POLL_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class SonySDCPCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to poll projector state."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.projector = pysdcp.Projector(entry.data[CONF_HOST])
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_POLL_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch power state from projector."""
        try:
            power = await self.hass.async_add_executor_job(
                self.projector.get_power
            )
        except Exception as err:
            raise UpdateFailed(f"Error communicating with projector: {err}") from err

        return {"power": power}
