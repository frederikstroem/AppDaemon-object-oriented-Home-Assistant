from helper.entity import Entity


class HaHelper(Entity):
    def __init__(self, api, ha_id, event_handler=None):
        super().__init__(api, ha_id)
        self.light_mode = None
        if event_handler is not None:
            self.api.listen_state(event_handler, self.ha_id)

    def get_state(self):
        return self.api.get_state(self.ha_id)
