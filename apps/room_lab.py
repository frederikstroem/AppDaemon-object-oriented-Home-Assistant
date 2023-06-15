import hassapi as hass
from helper.rooms.lab import Lab


class RoomLab(hass.Hass):
    def initialize(self):
        lab = Lab(self)
