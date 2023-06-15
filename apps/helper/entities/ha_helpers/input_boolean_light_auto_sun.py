import datetime as dt

from helper.entities.ha_helpers.input_boolean import InputBoolean
from helper.light_mode import LightModeModes


class InputBooleanLightAutoSun(InputBoolean):
    """Class to automate periods when the hallway light shouldn't auto turn on on movement detection.

    Args:
        api: Instance of the Home Assistant API.
        ha_id: ID of the input boolean in Home Assistant.
        offset_sunrise (int): Number of minutes to offset from sunrise time.
        offset_sunset (int): Number of minutes to offset from sunset time.
    """
    def __init__(self, api, ha_id, offset_sunrise=0, offset_sunset=0):
        super().__init__(api, ha_id, None)
        self.api.run_at_sunrise(self.event_sunrise)
        self.api.run_at_sunset(self.event_sunset, offset = dt.timedelta(minutes = -45).total_seconds())

    def event_sunrise(self, kwargs):
        self.turn_off()
        self.room.light_mode.set_light_mode(LightModeModes.WHITE)
        self.room.light_mode.set_light_intensity_before(255)
        self.api.log("Sunrise detected, turning off boolean.", log=self.room.log)

    def event_sunset(self, kwargs):
        self.turn_on()
        self.room.light_mode.set_light_mode(LightModeModes.WARM_WHITE)
        self.room.light_mode.set_light_intensity_before(int(255 * 0.75))
        self.api.log("Sunset detected, turning on boolean.", log=self.room.log)
