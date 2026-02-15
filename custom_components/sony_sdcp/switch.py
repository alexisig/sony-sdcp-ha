"""Switch platform for Sony SDCP projector power."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SonySDCPCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sony SDCP switch from a config entry."""
    coordinator: SonySDCPCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SonySDCPPowerSwitch(coordinator, entry)])


class SonySDCPPowerSwitch(CoordinatorEntity[SonySDCPCoordinator], SwitchEntity):
    """Representation of a Sony projector power switch."""

    _attr_has_entity_name = True
    _attr_name = "Power"
    _attr_icon = "mdi:projector"

    def __init__(
        self, coordinator: SonySDCPCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_power"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Sony",
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if projector is on."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("power")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the projector on."""
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_power, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the projector off."""
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_power, False
        )
        await self.coordinator.async_request_refresh()
