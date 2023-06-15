from helper.entities.ha_helper import HaHelper


class InputButton(HaHelper):
    def __init__(self, api, ha_id, event_handler=None):
        super().__init__(api, ha_id, event_handler)
