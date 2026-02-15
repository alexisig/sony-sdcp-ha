"""Switch platform for Sony SDCP projector."""

from __future__ import annotations

import logging
from typing import Any

from pysdcp_extended.protocol import (
    ACTIONS,
    COMMANDS,
    INPUT_LAG_REDUCTION as PROTO_INPUT_LAG_REDUCTION,
)

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SonySDCPCoordinator

_LOGGER = logging.getLogger(__name__)


def _make_device_info(entry: ConfigEntry) -> dict:
    return {
        "identifiers": {(DOMAIN, entry.entry_id)},
        "name": entry.data[CONF_NAME],
        "manufacturer": "Sony",
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sony SDCP switches from a config entry."""
    coordinator: SonySDCPCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SonySDCPPowerSwitch(coordinator, entry),
        SonySDCPPictureMutingSwitch(coordinator, entry),
        SonySDCPInputLagReductionSwitch(coordinator, entry),
    ])


# ---------------------------------------------------------------------------
# Power
# ---------------------------------------------------------------------------

class SonySDCPPowerSwitch(CoordinatorEntity[SonySDCPCoordinator], SwitchEntity):
    """Representation of a Sony projector power switch."""

    _attr_has_entity_name = True
    _attr_name = "Power"
    _attr_icon = "mdi:projector"

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_power"
        self._attr_device_info = _make_device_info(entry)

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("power")

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_power, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_power, False
        )
        await self.coordinator.async_request_refresh()


# ---------------------------------------------------------------------------
# Picture Muting
# ---------------------------------------------------------------------------

class SonySDCPPictureMutingSwitch(CoordinatorEntity[SonySDCPCoordinator], SwitchEntity):
    """Switch entity for picture muting (blank screen)."""

    _attr_has_entity_name = True
    _attr_name = "Picture Muting"
    _attr_icon = "mdi:projector-off"

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_picture_muting"
        self._attr_device_info = _make_device_info(entry)

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("muting")

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_muting, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_muting, False
        )
        await self.coordinator.async_request_refresh()


# ---------------------------------------------------------------------------
# Input Lag Reduction
# ---------------------------------------------------------------------------

class SonySDCPInputLagReductionSwitch(CoordinatorEntity[SonySDCPCoordinator], SwitchEntity):
    """Switch entity for input lag reduction."""

    _attr_has_entity_name = True
    _attr_name = "Input Lag Reduction"
    _attr_icon = "mdi:gamepad-variant"
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_input_lag_reduction"
        self._attr_device_info = _make_device_info(entry)
        self._is_on: bool | None = None

    @property
    def is_on(self) -> bool | None:
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["INPUT_LAG_REDUCTION"],
            PROTO_INPUT_LAG_REDUCTION["ON"],
        )
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["INPUT_LAG_REDUCTION"],
            PROTO_INPUT_LAG_REDUCTION["OFF"],
        )
        self._is_on = False
        self.async_write_ha_state()
