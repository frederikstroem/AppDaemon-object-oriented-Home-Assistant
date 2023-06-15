from enum import Enum

import globals
from helper.entities.controller import Controller


class AqaraSmartHomeCubeActions(Enum):
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    SLIDE = "slide"
    FLIP90 = "flip90"
    FLIP180 = "flip180"
    WAKEUP = "wakeup"

class AqaraSmartHomeCube(Controller):
    # def __init__(self, api, ha_id, action_map, default_action_map_rotate_left=True, default_action_map_rotate_right=True, default_action_map_slide=True, default_action_map_flip90=True, default_action_map_flip180=True):
    def __init__(self, api, ha_id, action_map):
        default_action_map = {
            AqaraSmartHomeCubeActions.ROTATE_LEFT: self.default_rotate_left,
            AqaraSmartHomeCubeActions.ROTATE_RIGHT: self.default_rotate_right,
            AqaraSmartHomeCubeActions.SLIDE: self.default_slide,
            AqaraSmartHomeCubeActions.FLIP90: self.default_flip90,
            AqaraSmartHomeCubeActions.FLIP180: self.default_flip180,
            AqaraSmartHomeCubeActions.WAKEUP: self.default_wakeup,
        }
        super().__init__(api, ha_id, AqaraSmartHomeCubeActions, action_map, default_action_map)

    def get_absolute_action_angle(self, ha_id):
        return abs(float(self.api.get_state(ha_id, attribute="action_angle")))

    def accelerated_action_angle(self, action_angle):
        # Use a piecewise function to create an acceleration curve.
        if action_angle <= 90:
            # Scale the action angle by 0.75 for values below or equal to 90 degrees.
            return_value = action_angle * 0.75
        else:
            # Apply an exponential acceleration curve for values above 90 degrees.
            # The curve will start accelerating from 90 degrees and reach 255 when the action angle is 180 degrees.
            return_value = 67.5 + (187.5 * ((action_angle - 90) / 90) ** 2)

        # Log the action angle before and after applying the acceleration.
        self.api.log(f"Applying acceleration to action angle: {action_angle} -> {return_value}", log=self.room.log)

        # Return the scaled or accelerated action angle.
        return return_value

    #
    # Default actions.
    #

    def default_rotate_left(self, ha_id):
        action_angle = self.get_absolute_action_angle(ha_id)
        scaled_angle = self.accelerated_action_angle(action_angle)
        self.api.log(f"Action angle for rotate_left: {scaled_angle}", log=self.room.log)
        self.light_mode.decrease_light_intensity(globals.angle_to_255(scaled_angle))

    def default_rotate_right(self, ha_id):
        action_angle = self.get_absolute_action_angle(ha_id)
        scaled_angle = self.accelerated_action_angle(action_angle)
        self.api.log(f"Action angle for rotate_right: {scaled_angle}", log=self.room.log)
        self.light_mode.increase_light_intensity(globals.angle_to_255(scaled_angle))

    def default_slide(self, ha_id):
        self.api.log("OOoohh Wee, I'm sliding!", log=self.room.log)
        self.light_mode.toggle_lights()

    def default_flip90(self, ha_id):
        self.api.log("I'm flipin' 90 degrees!", log=self.room.log)
        self.light_mode.next_light_mode()

    def default_flip180(self, ha_id):
        self.api.log("I'm flipin' 180 degrees!", log=self.room.log)
        self.light_mode.previous_light_mode()

    def default_wakeup(self, ha_id):
        # self.api.log("YO! I'm awake!", log=self.room.log)
        pass
