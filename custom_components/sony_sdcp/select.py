"""Select platform for Sony SDCP projector settings."""

from __future__ import annotations

import logging

from pysdcp_extended.protocol import (
    ACTIONS,
    CALIBRATION_PRESETS as PROTO_CALIBRATION_PRESETS,
    COMMANDS,
    DYNAMIC_RANGES as PROTO_DYNAMIC_RANGES,
    LAMP_CONTROL as PROTO_LAMP_CONTROL,
    ADVANCED_IRIS as PROTO_ADVANCED_IRIS,
    MOTIONFLOW as PROTO_MOTIONFLOW,
    HDR as PROTO_HDR,
    TWO_D_THREE_D_SELECT as PROTO_2D_3D,
    THREE_D_FORMATS as PROTO_3D_FORMATS,
    MENU_POSITIONS as PROTO_MENU_POSITIONS,
)

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ADVANCED_IRIS_MAP,
    ADVANCED_IRIS_MODES,
    ASPECT_RATIO_MAP,
    ASPECT_RATIOS,
    CALIBRATION_PRESET_MAP,
    CALIBRATION_PRESETS,
    DOMAIN,
    DYNAMIC_RANGE_MAP,
    DYNAMIC_RANGES,
    HDR_MAP,
    HDR_MODES,
    HDMI_INPUT_MAP,
    HDMI_INPUTS,
    LAMP_CONTROL_MAP,
    LAMP_CONTROLS,
    MENU_POSITION_MAP,
    MENU_POSITIONS,
    MOTIONFLOW_MAP,
    MOTIONFLOW_MODES,
    PICTURE_POSITION_MAP,
    PICTURE_POSITIONS,
    THREE_D_FORMAT_MAP,
    THREE_D_FORMATS,
    TWO_D_THREE_D_MAP,
    TWO_D_THREE_D_MODES,
)
from .coordinator import SonySDCPCoordinator

_LOGGER = logging.getLogger(__name__)


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
        SonySDCPCalibrationPresetSelect(coordinator, entry),
        SonySDCPDynamicRangeSelect(coordinator, entry, "HDMI 1", "HDMI1_DYNAMIC_RANGE", "hdmi1_dynamic_range"),
        SonySDCPDynamicRangeSelect(coordinator, entry, "HDMI 2", "HDMI2_DYNAMIC_RANGE", "hdmi2_dynamic_range"),
        SonySDCPLampControlSelect(coordinator, entry),
        SonySDCPAdvancedIrisSelect(coordinator, entry),
        SonySDCPMotionFlowSelect(coordinator, entry),
        SonySDCPHDRSelect(coordinator, entry),
        SonySDCP2D3DSelect(coordinator, entry),
        SonySDCP3DFormatSelect(coordinator, entry),
        SonySDCPMenuPositionSelect(coordinator, entry),
    ])


def _make_device_info(entry: ConfigEntry) -> dict:
    """Build device info dict."""
    return {
        "identifiers": {(DOMAIN, entry.entry_id)},
        "name": entry.data[CONF_NAME],
        "manufacturer": "Sony",
    }


# ---------------------------------------------------------------------------
# HDMI Input
# ---------------------------------------------------------------------------

class SonySDCPHDMIInputSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for HDMI input."""

    _attr_has_entity_name = True
    _attr_name = "HDMI Input"
    _attr_icon = "mdi:hdmi-port"
    _attr_options = HDMI_INPUTS

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_hdmi_input"
        self._attr_device_info = _make_device_info(entry)

    @property
    def current_option(self) -> str | None:
        if self.coordinator.data:
            return self.coordinator.data.get("input")
        return None

    async def async_select_option(self, option: str) -> None:
        hdmi_num = HDMI_INPUT_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_HDMI_input, hdmi_num
        )
        await self.coordinator.async_request_refresh()


# ---------------------------------------------------------------------------
# Aspect Ratio
# ---------------------------------------------------------------------------

class SonySDCPAspectRatioSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for aspect ratio."""

    _attr_has_entity_name = True
    _attr_name = "Aspect Ratio"
    _attr_icon = "mdi:aspect-ratio"
    _attr_options = ASPECT_RATIOS
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_aspect_ratio"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = ASPECT_RATIO_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_screen, "ASPECT_RATIO", value
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# Picture Position
# ---------------------------------------------------------------------------

class SonySDCPPicturePositionSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for picture position."""

    _attr_has_entity_name = True
    _attr_name = "Picture Position"
    _attr_icon = "mdi:image-move"
    _attr_options = PICTURE_POSITIONS
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_picture_position"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = PICTURE_POSITION_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector.set_screen, "PICTURE_POSITION", value
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# Calibration Preset
# ---------------------------------------------------------------------------

class SonySDCPCalibrationPresetSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for calibration preset."""

    _attr_has_entity_name = True
    _attr_name = "Calibration Preset"
    _attr_icon = "mdi:palette"
    _attr_options = CALIBRATION_PRESETS
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_calibration_preset"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = CALIBRATION_PRESET_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["CALIBRATION_PRESET"],
            PROTO_CALIBRATION_PRESETS[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# Dynamic Range (HDMI 1 / HDMI 2)
# ---------------------------------------------------------------------------

class SonySDCPDynamicRangeSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for HDMI dynamic range."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:contrast-box"
    _attr_options = DYNAMIC_RANGES
    _attr_current_option = None

    def __init__(
        self,
        coordinator: SonySDCPCoordinator,
        entry: ConfigEntry,
        hdmi_label: str,
        command_key: str,
        uid_suffix: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_name = f"{hdmi_label} Dynamic Range"
        self._attr_unique_id = f"{entry.entry_id}_{uid_suffix}"
        self._attr_device_info = _make_device_info(entry)
        self._command_key = command_key

    async def async_select_option(self, option: str) -> None:
        value = DYNAMIC_RANGE_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS[self._command_key],
            PROTO_DYNAMIC_RANGES[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# Lamp Control
# ---------------------------------------------------------------------------

class SonySDCPLampControlSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for lamp control."""

    _attr_has_entity_name = True
    _attr_name = "Lamp Control"
    _attr_icon = "mdi:lightbulb-outline"
    _attr_options = LAMP_CONTROLS
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_lamp_control"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = LAMP_CONTROL_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["LAMP_CONTROL"],
            PROTO_LAMP_CONTROL[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# Advanced Iris
# ---------------------------------------------------------------------------

class SonySDCPAdvancedIrisSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for advanced iris."""

    _attr_has_entity_name = True
    _attr_name = "Advanced Iris"
    _attr_icon = "mdi:eye-settings"
    _attr_options = ADVANCED_IRIS_MODES
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_advanced_iris"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = ADVANCED_IRIS_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["ADVANCED_IRIS"],
            PROTO_ADVANCED_IRIS[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# MotionFlow
# ---------------------------------------------------------------------------

class SonySDCPMotionFlowSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for MotionFlow."""

    _attr_has_entity_name = True
    _attr_name = "MotionFlow"
    _attr_icon = "mdi:motion"
    _attr_options = MOTIONFLOW_MODES
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_motionflow"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = MOTIONFLOW_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["MOTIONFLOW"],
            PROTO_MOTIONFLOW[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# HDR
# ---------------------------------------------------------------------------

class SonySDCPHDRSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for HDR."""

    _attr_has_entity_name = True
    _attr_name = "HDR"
    _attr_icon = "mdi:hdr"
    _attr_options = HDR_MODES
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_hdr"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = HDR_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["HDR"],
            PROTO_HDR[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# 2D/3D Display Select
# ---------------------------------------------------------------------------

class SonySDCP2D3DSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for 2D/3D display mode."""

    _attr_has_entity_name = True
    _attr_name = "2D/3D Display"
    _attr_icon = "mdi:video-3d"
    _attr_options = TWO_D_THREE_D_MODES
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_2d_3d_display"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = TWO_D_THREE_D_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["2D_3D_DISPLAY_SELECT"],
            PROTO_2D_3D[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# 3D Format
# ---------------------------------------------------------------------------

class SonySDCP3DFormatSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for 3D format."""

    _attr_has_entity_name = True
    _attr_name = "3D Format"
    _attr_icon = "mdi:video-3d-variant"
    _attr_options = THREE_D_FORMATS
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_3d_format"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = THREE_D_FORMAT_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["3D_FORMAT"],
            PROTO_3D_FORMATS[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()


# ---------------------------------------------------------------------------
# Menu Position
# ---------------------------------------------------------------------------

class SonySDCPMenuPositionSelect(CoordinatorEntity[SonySDCPCoordinator], SelectEntity):
    """Select entity for menu position."""

    _attr_has_entity_name = True
    _attr_name = "Menu Position"
    _attr_icon = "mdi:menu"
    _attr_options = MENU_POSITIONS
    _attr_current_option = None

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_menu_position"
        self._attr_device_info = _make_device_info(entry)

    async def async_select_option(self, option: str) -> None:
        value = MENU_POSITION_MAP[option]
        await self.hass.async_add_executor_job(
            self.coordinator.projector._send_command,
            ACTIONS["SET"],
            COMMANDS["MENU_POSITION"],
            PROTO_MENU_POSITIONS[value],
        )
        self._attr_current_option = option
        self.async_write_ha_state()
