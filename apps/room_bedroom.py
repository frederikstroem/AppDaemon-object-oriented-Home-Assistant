import hassapi as hass
from helper.rooms.bedroom import Bedroom


class RoomBedroom(hass.Hass):
    def initialize(self):
        bedroom = Bedroom(self)
