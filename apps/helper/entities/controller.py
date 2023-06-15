from helper.entity import Entity


class Controller(Entity):
    def __init__(self, api, ha_id, actions_enum, action_map, default_action_map=None):
        super().__init__(api, ha_id)
        self.actions_enum = actions_enum
        self.action_map = action_map
        self.default_action_map = default_action_map
        self.light_mode = None
        self.api.listen_state(self.handle_event, self.ha_id)

    def handle_event(self, entity, attribute, old, new, kwargs):
        if new != "":
            try:
                action = self.actions_enum(new)
                if action in self.action_map:
                    self.api.log(f"Action detected for {self.ha_id}: {new}.", log=self.room.log)
                    self.action_map[action](self.ha_id)
                elif self.default_action_map is not None and action in self.default_action_map:
                    self.api.log(f"Action {action} detected for {self.ha_id}, executing default function.", log=self.room.log)
                    self.default_action_map[action](self.ha_id)
                elif action in self.actions_enum:
                    self.api.log(f"Action for {self.ha_id} not implemented: {new}.", log=self.room.log)
            except ValueError:
                self.api.log(f"Unknown action detected for {self.ha_id}: {new}.", log=self.room.log)
