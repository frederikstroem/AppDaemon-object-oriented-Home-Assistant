from enum import Enum

from helper.entities.controller import Controller


class IkeaRemoteActions(Enum):
    TOGGLE = "toggle"
    BRIGHTNESS_UP_CLICK = "brightness_up_click"
    BRIGHTNESS_DOWN_CLICK = "brightness_down_click"
    ARROW_LEFT_CLICK = "arrow_left_click"
    ARROW_RIGHT_CLICK = "arrow_right_click"

class IkeaRemote(Controller):
    def __init__(self, api, ha_id, action_map):
        default_action_map = {
            IkeaRemoteActions.TOGGLE: self.default_toggle,
            IkeaRemoteActions.BRIGHTNESS_DOWN_CLICK: self.default_brightness_down,
            IkeaRemoteActions.BRIGHTNESS_UP_CLICK: self.default_brightness_up,
            IkeaRemoteActions.ARROW_LEFT_CLICK: self.default_arrow_left,
            IkeaRemoteActions.ARROW_RIGHT_CLICK: self.default_arrow_right,
        }
        super().__init__(api, ha_id, IkeaRemoteActions, action_map, default_action_map)

    def default_toggle(self, ha_id):
        self.light_mode.toggle_lights()

    def default_brightness_down(self, ha_id):
        self.light_mode.decrease_light_intensity(55)

    def default_brightness_up(self, ha_id):
        self.light_mode.increase_light_intensity(55)

    def default_arrow_left(self, ha_id):
        self.light_mode.previous_light_mode()

    def default_arrow_right(self, ha_id):
        self.light_mode.next_light_mode()
