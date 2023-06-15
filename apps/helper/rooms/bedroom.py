import globals
from helper.entities.controller import Controller
from helper.entities.controllers.aqara_smart_home_cube import (
    AqaraSmartHomeCube, AqaraSmartHomeCubeActions)
from helper.entities.ha_helpers.input_button import InputButton
from helper.entities.ha_helpers.input_button_light_toggle import InputButtonLightToggle
from helper.entities.light import Light
from helper.entities.lights.ikea_bulb import IkeaBulb
from helper.light_mode import LightMode, LightModeModes
from helper.room import Room


class Bedroom(Room):
    def __init__(self, api):

        ################################
        ##### Initialize the room. #####
        ############# START ############

        id = "bedroom"

        entities = [
            # Input buttons.
            InputButtonLightToggle(
                api,
                "input_button.bedroom_light_toggle"
            ),
            # Controllers.
            AqaraSmartHomeCube(
                api,
                "sensor.bedroom_controller_cube_action",
                {
                    # AqaraSmartHomeCubeActions.ROTATE_LEFT: self.event_AqaraSmartHomeCube_rotate_left,
                    # AqaraSmartHomeCubeActions.ROTATE_RIGHT: self.event_AqaraSmartHomeCube_rotate_right,
                    # AqaraSmartHomeCubeActions.SLIDE: self.event_cube_action_slide,
                    # AqaraSmartHomeCubeActions.FLIP90: self.event_cube_action_flip90,
                    # AqaraSmartHomeCubeActions.FLIP180: self.event_cube_action_flip180,
                },
            ),
            # Lights.
            IkeaBulb(
                api,
                "light.bedroom_light_ceiling"
            ),
        ]

        light_mode = LightMode(
            api,
            [entity for entity in entities if isinstance(entity, Light)],
            "input_number.bedroom_light_intensity",
            "input_select.bedroom_light_mode",
            "input_number.bedroom_light_mode_red",
            "input_number.bedroom_light_mode_green",
            "input_number.bedroom_light_mode_blue"
        )

        super().__init__(api, "bedroom", entities, light_mode)
        # TODO: FIX ME
        # This will be replaced, AFTER initialisation, super hacky, but it has to be done like this for now. :'(
        for entity in self.entities:
            entity.room = self

        self.api.log("West entered the chat. 🇺🇸", log="home_log")

        ############## END #############
