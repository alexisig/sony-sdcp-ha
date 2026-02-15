"""Constants for the Sony SDCP integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "sony_sdcp"

CONF_POLL_INTERVAL = "poll_interval"
DEFAULT_POLL_INTERVAL = 30

# --- Display lists (shown in HA UI) ---

HDMI_INPUTS = ["HDMI 1", "HDMI 2"]

ASPECT_RATIOS = ["Normal", "V Stretch", "Zoom 1.85", "Zoom 2.35", "Stretch", "Squeeze"]

PICTURE_POSITIONS = ["1.85", "2.35", "Custom 1", "Custom 2", "Custom 3", "Custom 4", "Custom 5"]

CALIBRATION_PRESETS = [
    "Cinema Film 1", "Cinema Film 2", "Reference", "TV",
    "Photo", "Game", "Bright Cinema", "Bright TV", "User",
]

DYNAMIC_RANGES = ["Auto", "Limited", "Full"]

LAMP_CONTROLS = ["Low", "High"]

ADVANCED_IRIS_MODES = ["Off", "Full", "Limited"]

MOTIONFLOW_MODES = ["Off", "Smooth High", "Smooth Low", "Impulse", "Combination", "True Cinema"]

HDR_MODES = ["Off", "On", "Auto"]

TWO_D_THREE_D_MODES = ["Auto", "3D", "2D"]

THREE_D_FORMATS = ["Simulated 3D", "Side by Side", "Over Under"]

MENU_POSITIONS = ["Bottom Left", "Center"]

# --- Mappings: HA display name -> pysdcp_extended protocol value ---

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
    "Custom 4": "CUSTOM_4",
    "Custom 5": "CUSTOM_5",
}

CALIBRATION_PRESET_MAP = {
    "Cinema Film 1": "CINEMA_FILM_1",
    "Cinema Film 2": "CINEMA_FILM_2",
    "Reference": "REF",
    "TV": "TV",
    "Photo": "PHOTO",
    "Game": "GAME",
    "Bright Cinema": "BRIGHT_CINEMA",
    "Bright TV": "BRIGHT_TV",
    "User": "USER",
}

DYNAMIC_RANGE_MAP = {
    "Auto": "AUTO",
    "Limited": "LIMITED",
    "Full": "FULL",
}

LAMP_CONTROL_MAP = {
    "Low": "LOW",
    "High": "HIGH",
}

ADVANCED_IRIS_MAP = {
    "Off": "OFF",
    "Full": "FULL",
    "Limited": "LIMITED",
}

MOTIONFLOW_MAP = {
    "Off": "OFF",
    "Smooth High": "SMOTH_HIGH",
    "Smooth Low": "SMOTH_LOW",
    "Impulse": "IMPULSE",
    "Combination": "COMBINATION",
    "True Cinema": "TRUE_CINEMA",
}

HDR_MAP = {
    "Off": "OFF",
    "On": "ON",
    "Auto": "AUTO",
}

TWO_D_THREE_D_MAP = {
    "Auto": "AUTO",
    "3D": "3D",
    "2D": "2D",
}

THREE_D_FORMAT_MAP = {
    "Simulated 3D": "SIMULATED_3D",
    "Side by Side": "SIDE_BY_SIDE",
    "Over Under": "OVER_UNDER",
}

MENU_POSITION_MAP = {
    "Bottom Left": "BOTTOM_LEFT",
    "Center": "CENTER",
}

# --- IR Commands: display name -> protocol key ---

IR_COMMANDS = {
    "Menu": "MENU",
    "Cursor Up": "CURSOR_UP",
    "Cursor Down": "CURSOR_DOWN",
    "Cursor Left": "CURSOR_LEFT",
    "Cursor Right": "CURSOR_RIGHT",
    "Cursor Enter": "CURSOR_ENTER",
    "Lens Shift Up": "LENS_SHIFT_UP",
    "Lens Shift Down": "LENS_SHIFT_DOWN",
    "Lens Shift Left": "LENS_SHIFT_LEFT",
    "Lens Shift Right": "LENS_SHIFT_RIGHT",
    "Lens Focus Far": "LENS_FOCUS_FAR",
    "Lens Focus Near": "LENS_FOCUS_NEAR",
    "Lens Zoom Large": "LENS_ZOOM_LARGE",
    "Lens Zoom Small": "LENS_ZOOM_SMALL",
}
