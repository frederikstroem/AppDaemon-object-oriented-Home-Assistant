from helper.entities.controller import Controller
from helper.entities.ha_helpers.input_button import InputButton
from helper.light_mode import LightMode

"""
    Room class
    Represents a room in the house.
    Attributes:
        api (API): The API object, hass.Hass object.
        id (str): The unique id of the room.
        entities (list): A list of entities (types) in the room.
"""
class Room:
    def __init__(self, api, id: str, entities, light_mode: LightMode):
        self.api = api
        self.id = id
        self.entities = entities
        self.light_mode = light_mode
        self.log = f"{self.id}_log"

        # register light mode & room for controllers and input buttons
        for entity in self.entities:
            if isinstance(entity, Controller) or isinstance(entity, InputButton):
                entity.room = self
                entity.light_mode = self.light_mode
        # register room for light mode
        self.light_mode.room = self

    def get_entity_by_ha_id(self, ha_id):
        for entity in self.entities:
            if entity.ha_id == ha_id:
                return entity
        return None

    def get_room_id(self):
        return self.id

    def get_light_mode(self):
        return self.light_mode
