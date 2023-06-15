from enum import Enum

from helper.entities.controller import Controller


class AqaraOppleSwitch3Actions(Enum):
    BUTTON_1_SINGLE = "button_1_single"
    BUTTON_1_DOUBLE = "button_1_double"
    BUTTON_1_TRIPLE = "button_1_triple"
    BUTTON_1_HOLD = "button_1_hold"
    BUTTON_1_RELEASE = "button_1_release"

    BUTTON_2_SINGLE = "button_2_single"
    BUTTON_2_DOUBLE = "button_2_double"
    BUTTON_2_TRIPLE = "button_2_triple"
    BUTTON_2_HOLD = "button_2_hold"
    BUTTON_2_RELEASE = "button_2_release"

    BUTTON_3_SINGLE = "button_3_single"
    BUTTON_3_DOUBLE = "button_3_double"
    BUTTON_3_TRIPLE = "button_3_triple"
    BUTTON_3_HOLD = "button_3_hold"
    BUTTON_3_RELEASE = "button_3_release"

    BUTTON_4_SINGLE = "button_4_single"
    BUTTON_4_DOUBLE = "button_4_double"
    BUTTON_4_TRIPLE = "button_4_triple"
    BUTTON_4_HOLD = "button_4_hold"
    BUTTON_4_RELEASE = "button_4_release"

    BUTTON_5_SINGLE = "button_5_single"
    BUTTON_5_DOUBLE = "button_5_double"
    BUTTON_5_TRIPLE = "button_5_triple"
    BUTTON_5_HOLD = "button_5_hold"
    BUTTON_5_RELEASE = "button_5_release"

    BUTTON_6_SINGLE = "button_6_single"
    BUTTON_6_DOUBLE = "button_6_double"
    BUTTON_6_TRIPLE = "button_6_triple"
    BUTTON_6_HOLD = "button_6_hold"
    BUTTON_6_RELEASE = "button_6_release"

class AqaraOppleSwitch3(Controller):
    def __init__(self, api, ha_id, action_map):
        default_action_map = {
            AqaraOppleSwitch3Actions.BUTTON_1_SINGLE: self.default_previous_light_mode,
            AqaraOppleSwitch3Actions.BUTTON_2_SINGLE: self.default_next_light_mode,
            AqaraOppleSwitch3Actions.BUTTON_3_SINGLE: self.default_light_intensity_decrease,
            AqaraOppleSwitch3Actions.BUTTON_4_SINGLE: self.default_light_intensity_increase,
            AqaraOppleSwitch3Actions.BUTTON_6_SINGLE: self.default_toggle,
        }
        super().__init__(api, ha_id, AqaraOppleSwitch3Actions, action_map, default_action_map)

    def default_previous_light_mode(self, ha_id):
        self.light_mode.previous_light_mode()

    def default_next_light_mode(self, ha_id):
        self.light_mode.next_light_mode()

    def default_light_intensity_decrease(self, ha_id):
        self.light_mode.decrease_light_intensity(55)

    def default_light_intensity_increase(self, ha_id):
        self.light_mode.increase_light_intensity(55)

    def default_toggle(self, ha_id):
        self.light_mode.toggle_lights()
