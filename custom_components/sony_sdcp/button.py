"""Button platform for Sony SDCP projector IR commands."""

from __future__ import annotations

from pysdcp_extended.protocol import ACTIONS, COMMANDS_IR

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, IR_COMMANDS
from .coordinator import SonySDCPCoordinator

# Map IR command keys to MDI icons
_IR_ICONS = {
    "MENU": "mdi:menu",
    "CURSOR_UP": "mdi:arrow-up-bold",
    "CURSOR_DOWN": "mdi:arrow-down-bold",
    "CURSOR_LEFT": "mdi:arrow-left-bold",
    "CURSOR_RIGHT": "mdi:arrow-right-bold",
    "CURSOR_ENTER": "mdi:check-bold",
    "LENS_SHIFT_UP": "mdi:arrow-up",
    "LENS_SHIFT_DOWN": "mdi:arrow-down",
    "LENS_SHIFT_LEFT": "mdi:arrow-left",
    "LENS_SHIFT_RIGHT": "mdi:arrow-right",
    "LENS_FOCUS_FAR": "mdi:image-filter-center-focus",
    "LENS_FOCUS_NEAR": "mdi:image-filter-center-focus-weak",
    "LENS_ZOOM_LARGE": "mdi:magnify-plus",
    "LENS_ZOOM_SMALL": "mdi:magnify-minus",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sony SDCP button entities from a config entry."""
    coordinator: SonySDCPCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SonySDCPIRButton(coordinator, entry, display_name, command_key)
        for display_name, command_key in IR_COMMANDS.items()
    ])


class SonySDCPIRButton(CoordinatorEntity[SonySDCPCoordinator], ButtonEntity):
    """Button entity for an IR command."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SonySDCPCoordinator,
        entry: ConfigEntry,
        display_name: str,
        command_key: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_name = display_name
        self._attr_unique_id = f"{entry.entry_id}_{command_key.lower()}"
        self._attr_icon = _IR_ICONS.get(command_key, "mdi:remote")
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Sony",
        }
        self._command_key = command_key

    async def async_press(self) -> None:
        """Send the IR command."""
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS_IR[self._command_key],
        )
