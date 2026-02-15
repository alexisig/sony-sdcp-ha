"""Config flow for Sony SDCP."""

from __future__ import annotations

import logging
from typing import Any

import pysdcp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_NAME

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_NAME): str,
    }
)


class SonySDCPConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sony SDCP."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                projector = pysdcp.Projector(user_input[CONF_HOST])
                await self.hass.async_add_executor_job(projector.get_power)
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
