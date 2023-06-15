from enum import Enum

from helper.entities.sensor import DiscreteSensor


class PersonStates(Enum):
    HOME = "home"
    AWAY = "not_home"

class Person(DiscreteSensor):
    def __init__(self, api, ha_id, event_map):
        super().__init__(api, ha_id, PersonStates, event_map)
