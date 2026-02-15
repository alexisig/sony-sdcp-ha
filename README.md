# Sony SDCP - Home Assistant Integration

Custom [Home Assistant](https://www.home-assistant.io/) integration to control Sony projectors via the SDCP (Simple Display Control Protocol) over IP.

Based on the [pySDCP-extended](https://github.com/kennymc-c/pySDCP-extended) library.

## Features

### Switches
- **Power** — Turn your projector on/off.
- **Picture Muting** — Blank the screen.
- **Input Lag Reduction** — Toggle input lag reduction (game mode).

### Selects
- **HDMI Input** — Switch between HDMI 1 and HDMI 2.
- **Aspect Ratio** — Normal, V Stretch, Zoom 1.85, Zoom 2.35, Stretch, Squeeze.
- **Picture Position** — 1.85, 2.35, Custom 1-5.
- **Calibration Preset** — Cinema Film 1/2, Reference, TV, Photo, Game, Bright Cinema, Bright TV, User.
- **HDMI 1 Dynamic Range** — Auto, Limited, Full.
- **HDMI 2 Dynamic Range** — Auto, Limited, Full.
- **Lamp Control** — Low, High.
- **Advanced Iris** — Off, Full, Limited.
- **MotionFlow** — Off, Smooth High, Smooth Low, Impulse, Combination, True Cinema.
- **HDR** — Off, On, Auto.
- **2D/3D Display** — Auto, 3D, 2D.
- **3D Format** — Simulated 3D, Side by Side, Over Under.
- **Menu Position** — Bottom Left, Center.

### Sensors
- **Lamp Hours** — Current lamp usage in hours.

### Buttons (IR Commands)
- **Menu**, **Cursor Up/Down/Left/Right/Enter**
- **Lens Shift Up/Down/Left/Right**
- **Lens Focus Far/Near**
- **Lens Zoom Large/Small**

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant.
2. Go to **Integrations** > **Custom repositories**.
3. Add `https://github.com/alexisig/sony-sdcp-ha` with category **Integration**.
4. Search for "Sony SDCP" and install it.
5. Restart Home Assistant.

### Manual

1. Copy the `custom_components/sony_sdcp` folder into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.

## Configuration

1. Go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for **Sony SDCP**.
3. Enter the IP address and a name for your projector.

The projector must be reachable on your local network. The integration will attempt a connection during setup.

## Compatibility

This integration should work with Sony projectors that support the SDCP/PJ Talk protocol, including VPL-HW65ES, VPL-VW100, VPL-VW260, VPL-VW270, VPL-VW285, VPL-VW315, VPL-VW320, VPL-VW328, VPL-VW365, VPL-VW515, VPL-VW520, VPL-VW528, VPL-VW665, and VPL-XW6100.
