"""DataUpdateCoordinator for Sony SDCP."""

from __future__ import annotations

from datetime import timedelta
import logging

import pysdcp_extended

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
        self.projector = pysdcp_extended.Projector(entry.data[CONF_HOST])
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_POLL_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch state from projector."""
        try:
            power = await self.hass.async_add_executor_job(
                self.projector.get_power
            )
        except Exception as err:
            raise UpdateFailed(f"Error communicating with projector: {err}") from err

        data: dict = {"power": power}

        # Only poll additional data when projector is on
        if power:
            try:
                data["muting"] = await self.hass.async_add_executor_job(
                    self.projector.get_muting
                )
            except Exception:
                _LOGGER.debug("Failed to get muting state")

            try:
                data["lamp_hours"] = await self.hass.async_add_executor_job(
                    self.projector.get_lamp_hours
                )
            except Exception:
                _LOGGER.debug("Failed to get lamp hours")

            try:
                data["input"] = await self.hass.async_add_executor_job(
                    self.projector.get_input
                )
            except Exception:
                _LOGGER.debug("Failed to get input")

        return data
