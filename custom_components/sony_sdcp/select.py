"""Select platform for Sony SDCP projector settings."""

from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ASPECT_RATIOS,
    DOMAIN,
    HDMI_INPUTS,
    PICTURE_POSITIONS,
)
from .coordinator import SonySDCPCoordinator

_LOGGER = logging.getLogger(__name__)

# Maps HA display values to pySDCP arguments
HDMI_INPUT_MAP = {
    "HDMI 1": 1,
    "HDMI 2": 2,
}

ASPECT_RATIO_MAP = {
    "Normal": "NORMAL",
    "V Stretch": "V_STRETCH",
    "Zoom 1.85": "ZOOM_1_85",
    "Zoom 2.35": "ZOOM_2_35",
    "Stretch": "STRETCH",
    "Squeeze": "SQUEEZE",
}

PICTURE_POSITION_MAP = {
    "1.85": "1_85",
    "2.35": "2_35",
    "Custom 1": "CUSTOM_1",
    "Custom 2": "CUSTOM_2",
    "Custom 3": "CUSTOM_3",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sony SDCP select entities from a config entry."""
    coordinator: SonySDCPCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SonySDCPHDMIInputSelect(coordinator, entry),
        SonySDCPAspectRatioSelect(coordinator, entry),
        SonySDCPPicturePositionSelect(coordinator, entry),
    ])


class SonySDCPHDMIInputSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for HDMI input."""

    _attr_has_entity_name = True
    _attr_name = "HDMI Input"
    _attr_icon = "mdi:hdmi-port"
    _attr_options = HDMI_INPUTS
    _attr_current_option = None

    def __init__(
        self, coordinator: SonySDCPCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_hdmi_input"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Sony",
        }

    async def async_select_option(self, option: str) -> None:
        """Change the HDMI input."""
        hdmi_num = HDMI_INPUT_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_HDMI_input, hdmi_num
        )
        self._attr_current_option = option
        self.async_write_ha_state()


class SonySDCPAspectRatioSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for aspect ratio."""

    _attr_has_entity_name = True
    _attr_name = "Aspect Ratio"
    _attr_icon = "mdi:aspect-ratio"
    _attr_options = ASPECT_RATIOS
    _attr_current_option = None

    def __init__(
        self, coordinator: SonySDCPCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_aspect_ratio"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Sony",
        }

    async def async_select_option(self, option: str) -> None:
        """Change the aspect ratio."""
        value = ASPECT_RATIO_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_screen, "ASPECT_RATIO", value
        )
        self._attr_current_option = option
        self.async_write_ha_state()


class SonySDCPPicturePositionSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for picture position."""

    _attr_has_entity_name = True
    _attr_name = "Picture Position"
    _attr_icon = "mdi:image-move"
    _attr_options = PICTURE_POSITIONS
    _attr_current_option = None

    def __init__(
        self, coordinator: SonySDCPCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_picture_position"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Sony",
        }

    async def async_select_option(self, option: str) -> None:
        """Change the picture position."""
        value = PICTURE_POSITION_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_screen, "PICTURE_POSITION", value
        )
        self._attr_current_option = option
        self.async_write_ha_state()
