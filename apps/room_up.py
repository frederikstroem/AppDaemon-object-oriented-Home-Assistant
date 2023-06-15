import hassapi as hass
from helper.rooms.up import Up


class RoomUp(hass.Hass):
    def initialize(self):
        up = Up(self)
