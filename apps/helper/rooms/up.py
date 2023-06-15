import globals
from helper.entities.controller import Controller
from helper.entities.controllers.aqara_smart_home_cube import (
    AqaraSmartHomeCube, AqaraSmartHomeCubeActions)
from helper.entities.ha_helpers.input_button import InputButton
from helper.entities.ha_helpers.input_button_light_toggle import InputButtonLightToggle
from helper.entities.light import Light
from helper.entities.lights.ikea_bulb import IkeaBulb
from helper.entities.lights.switch_light import SwitchLight
from helper.entities.sensors.ikea_motion_sensor import (IkeaMotionSensor,
                                                        IkeaMotionSensorStates)
from helper.light_mode import LightMode, LightModeModes
from helper.room import Room


class Up(Room):
    def __init__(self, api):

        ################################
        ##### Initialize the room. #####
        ############# START ############

        id = "up"

        entities = [
            # Input buttons.
            InputButtonLightToggle(
                api,
                "input_button.up_light_toggle"
            ),
            # Sensors.
            IkeaMotionSensor(
                api,
                "binary_sensor.up_ir_stairs_occupancy",
                {
                    IkeaMotionSensorStates.ON: self.event_IkeaMotionSensor_on,
                    IkeaMotionSensorStates.OFF: self.event_IkeaMotionSensor_off,
                }
            ),
            # Controllers.
            AqaraSmartHomeCube(
                api,
                "sensor.up_controller_cube_action",
                {
                    # AqaraSmartHomeCubeActions.ROTATE_LEFT: self.event_AqaraSmartHomeCube_rotate_left,
                    # AqaraSmartHomeCubeActions.ROTATE_RIGHT: self.event_AqaraSmartHomeCube_rotate_right,
                    # AqaraSmartHomeCubeActions.SLIDE: self.event_cube_action_slide,
                    # AqaraSmartHomeCubeActions.FLIP90: self.event_cube_action_flip90,
                    # AqaraSmartHomeCubeActions.FLIP180: self.event_cube_action_flip180,
                }
            ),
            # Lights.
            SwitchLight(
                api,
                "switch.up_light_neon_cactus",
            ),
            IkeaBulb(
                api,
                "light.up_light_north",
            ),
            IkeaBulb(
                api,
                "light.up_light_south",
            ),
        ]

        light_mode = LightMode(
            api,
            [entity for entity in entities if isinstance(entity, Light)],
            "input_number.up_light_intensity",
            "input_select.up_light_mode",
            "input_number.up_light_mode_red",
            "input_number.up_light_mode_green",
            "input_number.up_light_mode_blue"
        )

        super().__init__(api, "up", entities, light_mode)
        # TODO: FIX ME
        # This will be replaced, AFTER initialisation, super hacky, but it has to be done like this for now. :'(
        for entity in self.entities:
            entity.room = self

        self.api.log(f"Upstairs initialized, a part of {globals.HOME_NAME}.", log="home_log")

        ############## END #############

    ################################
    ####### Event callbacks. #######
    ############# START ############

    def event_IkeaMotionSensor_on(self, ha_id):
        self.api.log("Motion detected, turning on cactus.", log=self.log)
        self.get_entity_by_ha_id("switch.up_light_neon_cactus").turn_on()

    def event_IkeaMotionSensor_off(self, ha_id):
        self.api.log("No motion detected, turning off cactus.", log=self.log)
        self.get_entity_by_ha_id("switch.up_light_neon_cactus").turn_off()

    ############## END #############
