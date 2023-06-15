from helper.entities.light import Light


class IkeaBulb(Light):
    def __init__(self, api, ha_id):
        super().__init__(api, ha_id)

    def turn_on(self, brightness, rgb):
        """
        Turn on the IkeaBulb with the specified brightness and RGB color.

        :param brightness: The brightness value from 0 to 255.
        :type brightness: int
        :param rgb: A tuple containing the red, green, and blue color values, each from 0 to 255.
        :type rgb: tuple
        """

        self.api.turn_on(self.ha_id, brightness=brightness, rgb_color=rgb)
