import globals
from helper.entities.controller import Controller
from helper.entities.ha_helpers.input_boolean import InputBoolean
from helper.entities.ha_helpers.input_boolean_light_auto_sun import InputBooleanLightAutoSun
from helper.entities.ha_helpers.input_button import InputButton
from helper.entities.ha_helpers.input_button_light_toggle import InputButtonLightToggle
from helper.entities.light import Light
from helper.entities.lights.ikea_bulb import IkeaBulb
from helper.entities.lights.switch_light import SwitchLight
from helper.entities.sensors.ikea_motion_sensor import (IkeaMotionSensor,
                                                        IkeaMotionSensorStates)
from helper.light_mode import LightMode, LightModeModes

from helper.entities.controllers.ikea_switch import (IkeaSwitch, IkeaSwitchActions)
from helper.room import Room


class Hall(Room):
    def __init__(self, api):

        ################################
        ##### Initialize the room. #####
        ############# START ############

        id = "hall"

        entities = [
            # Input buttons.
            InputButtonLightToggle(
                api,
                "input_button.hall_light_toggle"
            ),
            # Input booleans.
            InputBooleanLightAutoSun(
                api,
                "input_boolean.hall_light_auto",
                offset_sunrise=30,
                offset_sunset=30
            ),
            # Controllers.
            IkeaSwitch(
                api,
                "sensor.hall_controller_ikea_switch_action",
            ),
            # Sensors.
            IkeaMotionSensor(
                api,
                "binary_sensor.hall_ir_by_rooms_occupancy",
                {
                    IkeaMotionSensorStates.ON: self.event_IkeaMotionSensor_on,
                    IkeaMotionSensorStates.OFF: self.event_IkeaMotionSensor_off,
                }
            ),
            # Lights.
            IkeaBulb(
                api,
                "light.hall_light_ceiling",
            ),
        ]

        light_mode = LightMode(
            api,
            [entity for entity in entities if isinstance(entity, Light)],
            "input_number.hall_light_intensity",
            "input_select.hall_light_mode",
            "input_number.hall_light_mode_red",
            "input_number.hall_light_mode_green",
            "input_number.hall_light_mode_blue"
        )

        super().__init__(api, "hall", entities, light_mode)
        # TODO: FIX ME
        # This will be replaced, AFTER initialisation, super hacky, but it has to be done like this for now. :'(
        for entity in self.entities:
            entity.room = self

        self.api.log(f"Hallway initialized, a part of {globals.HOME_NAME}.", log="home_log")

        ############## END #############

    ################################
    ####### Event callbacks. #######
    ############# START ############

    def event_IkeaMotionSensor_on(self, ha_id):
        self.api.log("Motion detected, turning on lights.", log=self.log)
        # self.get_entity_by_ha_id("light.hall_light_ceiling").turn_on()
        if self.get_entity_by_ha_id("input_boolean.hall_light_auto").get_state() == "on":
            self.light_mode.turn_on_lights()

    def event_IkeaMotionSensor_off(self, ha_id):
        self.api.log("No motion detected, turning off lights.", log=self.log)
        # self.get_entity_by_ha_id("light.hall_light_ceiling").turn_off()
        if self.get_entity_by_ha_id("input_boolean.hall_light_auto").get_state() == "on":
            self.light_mode.turn_off_lights()

    ############## END #############
