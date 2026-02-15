"""Sensor platform for Sony SDCP projector."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SonySDCPCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sony SDCP sensors from a config entry."""
    coordinator: SonySDCPCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SonySDCPLampHoursSensor(coordinator, entry)])


class SonySDCPLampHoursSensor(CoordinatorEntity[SonySDCPCoordinator], SensorEntity):
    """Sensor entity for lamp hours."""

    _attr_has_entity_name = True
    _attr_name = "Lamp Hours"
    _attr_icon = "mdi:clock-outline"
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, coordinator: SonySDCPCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_lamp_hours"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Sony",
        }

    @property
    def native_value(self) -> int | None:
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get("lamp_hours")
        if value is not None:
            return int(value)
        return None
