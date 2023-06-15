from helper.entities.ha_helpers.input_button import InputButton


class InputButtonLightToggle(InputButton):
    def __init__(self, api, ha_id):
        super().__init__(api, ha_id, self.handle_event)

    def handle_event(self, entity, attribute, old, new, kwargs):
        if new != "" and new != old:
            try:
                # self.api.log(f"Action {new} detected, executing default function toggling lights.", log=self.room.log)
                self.api.log(f"Action detected for {entity}: {new}", log=self.room.log)
                self.room.light_mode.toggle_lights()
            except ValueError:
                self.api.log(f"Unknown action: {new}", log="error_log")
