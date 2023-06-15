import hassapi as hass
from helper.rooms.hall import Hall


class RoomHall(hass.Hass):
    def initialize(self):
        hall = Hall(self)
