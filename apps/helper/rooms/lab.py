import globals
from helper.entities.controller import Controller
from helper.entities.controllers.aqara_opple_switch_3 import (
    AqaraOppleSwitch3, AqaraOppleSwitch3Actions)
from helper.entities.controllers.aqara_smart_home_cube import (
    AqaraSmartHomeCube, AqaraSmartHomeCubeActions)
from helper.entities.controllers.ikea_remote import (IkeaRemote,
                                                     IkeaRemoteActions)
from helper.entities.ha_helpers.input_button import InputButton
from helper.entities.ha_helpers.input_button_light_toggle import InputButtonLightToggle
from helper.entities.light import Light
from helper.entities.lights.ikea_bulb import IkeaBulb
from helper.entities.lights.switch_light import SwitchLight
from helper.entities.relay import Relay
from helper.entities.sensors.aubess_smart_plug import AubessSmartPlug
from helper.entities.sensors.person import Person, PersonStates
from helper.light_mode import LightMode, LightModeModes
from helper.room import Room


class Lab(Room):
    def __init__(self, api):

        ################################
        ##### Initialize the room. #####
        ############# START ############

        id = "lab"

        entities = [
            # Input buttons.
            InputButtonLightToggle(
                api,
                "input_button.lab_light_toggle"
            ),
            # Sensors.
            Person(
                api,
                "person.frederik_holm_strom",
                {
                    PersonStates.AWAY: self.event_person_away,
                }
            ),
            AubessSmartPlug(
                api,
                "sensor.lab_relay_desktop_power",
                self.event_desktop_power_change
            ),
            # Controllers.
            AqaraOppleSwitch3(
                api,
                "sensor.lab_controller_desk_action",
                {}
            ),
            AqaraSmartHomeCube(
                api,
                "sensor.lab_controller_cube_action",
                {},
            ),
            IkeaRemote(
                api,
                "sensor.lab_controller_by_door_action",
                {}
            ),
            # Lights.
            IkeaBulb(
                api,
                "light.lab_light_ceiling"
            ),
            IkeaBulb(
                api,
                "light.lab_light_by_mirror"
            ),
            SwitchLight(
                api,
                "switch.lab_light_neon_rocket"
            ),
            # Relays.
            Relay(
                api,
                "switch.lab_relay_speakers"
            ),
        ]

        light_mode = LightMode(
            api,
            [entity for entity in entities if isinstance(entity, Light)],
            "input_number.lab_light_intensity",
            "input_select.lab_light_mode",
            "input_number.lab_light_mode_red",
            "input_number.lab_light_mode_green",
            "input_number.lab_light_mode_blue"
        )

        super().__init__(api, "lab", entities, light_mode)
        # TODO: FIX ME
        # This will be replaced, AFTER initialisation, super hacky, but it has to be done like this for now. :'(
        for entity in self.entities:
            entity.room = self

        # for ha_id in self.ha_id_watch_list:
        #     self.api.listen_state(self.light_mode_event, ha_id)
        self.light_mode.event_any_light_mode_change(self.event_any_light_mode_change)

        self.api.log(f"Lab initialized, the brain of our {globals.HOME_NAME}.", log="home_log")

        ############## END #############

    ################################
    ####### Event callbacks. #######
    ############# START ############

    def event_person_away(self, ha_id):
        self.api.log("Strøm left Home, turning off the lights in lab.", log=self.log)
        self.light_mode.set_light_intensity(0)

    def event_desktop_power_change(self, new_value, old_value):
        # self.api.log(f"Desktop power changed to {new_value}W.", log=self.log)
        speaker_relay = self.get_entity_by_ha_id("switch.lab_relay_speakers")
        if new_value > 18 and old_value <= 18:
            self.api.log(f"Desktop power changed to {new_value}W, was {old_value}W, turning on speakers.", log=self.log)
            speaker_relay.turn_on()
        elif new_value <= 18 and old_value > 18:
            self.api.log(f"Desktop power changed to {new_value}W, was {old_value}W, turning off speakers.", log=self.log)
            speaker_relay.turn_off()

    def event_any_light_mode_change(self, entity, attribute, old, new, kwargs):
        self.api.log(f"Entity {entity} changed light mode to {new}.", log=self.log)
        if self.light_mode.get_light_intensity() > globals.decimal_to_255(0.45):
            self.get_entity_by_ha_id("switch.lab_light_neon_rocket").turn_on()
        else:
            self.get_entity_by_ha_id("switch.lab_light_neon_rocket").turn_off()

        ############## END #############
