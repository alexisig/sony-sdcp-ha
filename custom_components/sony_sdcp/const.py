"""Constants for the Sony SDCP integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "sony_sdcp"

CONF_POLL_INTERVAL = "poll_interval"
DEFAULT_POLL_INTERVAL = 30

HDMI_INPUTS = ["HDMI 1", "HDMI 2"]

ASPECT_RATIOS = ["Normal", "V Stretch", "Zoom 1.85", "Zoom 2.35", "Stretch", "Squeeze"]

PICTURE_POSITIONS = ["1.85", "2.35", "Custom 1", "Custom 2", "Custom 3"]
