from enum import Enum

from helper.entities.light import Light
from helper.entities.lights.ikea_bulb import IkeaBulb


class LightModeModes(Enum):
    WARM = "Warm"
    WARM_WHITE = "Warm White"
    WHITE = "White"
    RED = "Red"
    PINK = "Pink"
    CUSTOM = "Custom"

# ha_id: Home Assistant entity ID
class LightMode:
    def __init__(self, api, light_entities, light_intensity, light_mode, light_mode_red, light_mode_green, light_mode_blue):
        self.api = api
        # This will be replaced, AFTER initialisation, super hacky, but it has to be done like this for now. :'(
        self.room = None
        self.light_entities = light_entities
        self.light_intensity = light_intensity
        self.light_intensity_before = round(255 * 0.75)    # Used to restore light intensity if light turns off. Is therefore between 1-255.
        self.light_mode = light_mode
        self.light_mode_red = light_mode_red
        self.light_mode_green = light_mode_green
        self.light_mode_blue = light_mode_blue

        self.ha_id_watch_list = [
            self.light_intensity,
            self.light_mode,
            self.light_mode_red,
            self.light_mode_green,
            self.light_mode_blue
        ]
        for ha_id in self.ha_id_watch_list:
            self.api.listen_state(self.event_apply_light_mode_settings, ha_id)

    ################################
    ########### Setters. ###########
    ############# START ############

    def set_light_intensity(self, light_intensity: int):
        """Set light intensity.

        Args:
            light_intensity (int): Light intensity value between 0-255.
        """
        # Check if the provided light_intensity is within the valid range (0-255)
        if 0 <= light_intensity <= 255:
            # Get the current light intensity
            current_intensity = self.get_light_intensity()
            # If the new light intensity is 0 and the current intensity is greater than 0, store the current intensity
            if light_intensity == 0 and current_intensity > 0:
                self.light_intensity_before = current_intensity
            # If the new light intensity is greater than 0 and the current intensity is 0, update the previous intensity
            elif light_intensity > 0 and current_intensity == 0:
                self.light_intensity_before = light_intensity
            # Set the new light intensity
            self.api.set_state(self.light_intensity, state=int(round(light_intensity)))
        else:
            # Log an error if the provided light_intensity is outside the valid range (0-255)
            self.api.log(f"Invalid light intensity value: {light_intensity}. Must be between 0-255.", log="error_log")

    def set_light_intensity_before(self, light_intensity_before: int):
        """Set light intensity before.

        Args:
            light_intensity_before (int): Light intensity value between 0-255.
        """
        # Check if the provided light_intensity_before is within the valid range (0-255)
        if 0 <= light_intensity_before <= 255:
            # Set the new light intensity before
            self.light_intensity_before = light_intensity_before
        else:
            # Log an error if the provided light_intensity_before is outside the valid range (0-255)
            self.api.log(f"Invalid light intensity before value: {light_intensity_before}. Must be between 0-255.", log="error_log")

    def increase_light_intensity(self, amount: int):
        """Increase light intensity by a given amount.

        Args:
            amount (int): Amount to increase light intensity by.
        """
        current_intensity = self.get_light_intensity()
        new_intensity = min(current_intensity + amount, 255)
        self.set_light_intensity(new_intensity)

    def decrease_light_intensity(self, amount: int):
        """Decrease light intensity by a given amount.

        Args:
            amount (int): Amount to decrease light intensity by.
        """
        current_intensity = self.get_light_intensity()
        new_intensity = max(current_intensity - amount, 0)
        self.set_light_intensity(new_intensity)

    def turn_on_lights(self):
        """Turn on lights."""
        self.set_light_intensity(self.light_intensity_before)

    def turn_off_lights(self):
        """Turn off lights."""
        self.set_light_intensity(0)

    def toggle_lights(self):
        """Toggle lights."""
        if self.get_light_intensity() > 0:
            self.turn_off_lights()
        else:
            self.turn_on_lights()

    def set_light_mode(self, light_mode: LightModeModes):
        """Set light mode.

        Args:
            light_mode (LightModeModes): Light mode value present in the LightModeModes enum.
        """
        self.api.set_state(self.light_mode, state=light_mode.value)

    def set_light_mode_by_index(self, index: int):
        """Set light mode by index.

        Args:
            index (int): Index of the light mode in the LightModeModes enumeration.
        """
        if 0 <= index < len(LightModeModes):
            light_mode = list(LightModeModes)[index]
            self.set_light_mode(light_mode)
        else:
            self.api.log(f"Invalid light mode index: {index}. Must be between 0-{len(LightModeModes) - 1}.", log="error_log")

    def next_light_mode(self):
        """Set the next light mode."""
        current_index = self.get_light_mode_index()
        next_index = (current_index + 1) % len(LightModeModes)
        next_mode = list(LightModeModes)[next_index]
        self.set_light_mode(next_mode)

    def previous_light_mode(self):
        """Set the previous light mode."""
        current_index = self.get_light_mode_index()
        previous_index = (current_index - 1) % len(LightModeModes)
        previous_mode = list(LightModeModes)[previous_index]
        self.set_light_mode(previous_mode)

    def set_light_mode_red(self, red: int):
        """Set light mode red value.

        Args:
            red (int): Red value between 0-255.
        """
        if 0 <= red <= 255:
            self.api.set_state(self.light_mode_red, state=int(round(red)))
        else:
            self.api.log(f"Invalid light mode red value: {red}. Must be between 0-255.", log="error_log")

    def set_light_mode_green(self, green: int):
        """Set light mode green value.

        Args:
            green (int): Green value between 0-255.
        """
        if 0 <= green <= 255:
            self.api.set_state(self.light_mode_green, state=int(round(green)))
        else:
            self.api.log(f"Invalid light mode green value: {green}. Must be between 0-255.", log="error_log")

    def set_light_mode_blue(self, blue: int):
        """Set light mode blue value.

        Args:
            blue (int): Blue value between 0-255.
        """
        if 0 <= blue <= 255:
            self.api.set_state(self.light_mode_blue, state=int(round(blue)))
        else:
            self.api.log(f"Invalid light mode blue value: {blue}. Must be between 0-255.", log="error_log")

    ############# END ##############
    ################################
    ####### Register events. #######
    ############# START ############

    def event_any_light_mode_change(self, event):
        # Register event for any light mode change.
        # self.ha_id_watch_list
        for ha_id in self.ha_id_watch_list:
            self.api.listen_state(event, ha_id)

    def event_light_intensity_changed(self, event):
        # Register event for light intensity changed.
        self.api.listen_state(event, self.light_intensity)

    ############# END ##############
    ################################
    ########### Getters. ###########
    ############# START ############

    def get_light_intensity(self):
        """Get light intensity.

        Returns:
            int: Light intensity value between 0-255.
        """
        return int(round(float(self.api.get_state(self.light_intensity))))

    def is_light_on(self):
        """Check if light is on.

        Returns:
            bool: True if light is on, False otherwise.
        """
        return self.get_light_intensity() > 0

    def get_light_mode(self):
        """Get light mode.

        Returns:
            LightModeModes: Light mode value present in the LightModeModes enum.
        """
        return LightModeModes(self.api.get_state(self.light_mode))

    def get_light_mode_index(self):
        """Get the index of the current light mode in the LightModeModes enumeration.

        Returns:
            int: Index of the current light mode.
        """
        current_mode = self.get_light_mode()
        return list(LightModeModes).index(current_mode)

    def get_light_mode_red(self):
        """Get light mode red value.

        Returns:
            int: Red value between 0-255.
        """
        return int(round(float(self.api.get_state(self.light_mode_red))))

    def get_light_mode_green(self):
        """Get light mode green value.

        Returns:
            int: Green value between 0-255.
        """
        return int(round(float(self.api.get_state(self.light_mode_green))))

    def get_light_mode_blue(self):
        """Get light mode blue value.

        Returns:
            int: Blue value between 0-255.
        """
        return int(round(float(self.api.get_state(self.light_mode_blue))))

    ############# END ##############
    ################################
    ####### Event callbacks. #######
    ############# START ############

    def event_apply_light_mode_settings(self, entity, attribute, old, new, kwargs):
        """Apply the light mode settings currently present in this class."""

        self.api.log(f"Applying light mode settings for {entity}, was {old}, now {new}.", log=self.room.log)

        light_mode = self.get_light_mode()

        for light_entity in self.light_entities:
            if isinstance(light_entity, IkeaBulb):
                match light_mode:
                    case LightModeModes.WHITE:
                        light_entity.turn_on(self.get_light_intensity(), (255, 180, 117))
                    case LightModeModes.WARM_WHITE:
                        light_entity.turn_on(self.get_light_intensity(), (255, 146, 39))
                    case LightModeModes.WARM:
                        light_entity.turn_on(self.get_light_intensity(), (255, 106, 67))
                    case LightModeModes.RED:
                        light_entity.turn_on(self.get_light_intensity(), (255, 0, 0))
                    case LightModeModes.PINK:
                        light_entity.turn_on(self.get_light_intensity(), (255, 0, 255))
                    case LightModeModes.CUSTOM:
                        light_entity.turn_on(self.get_light_intensity(), (self.get_light_mode_red(), self.get_light_mode_green(), self.get_light_mode_blue()))
                    case _:
                        # Handle unexpected light mode values
                        self.api.log(f"Unexpected light mode value: {light_mode}.", log="error_log")

    ############## END #############
