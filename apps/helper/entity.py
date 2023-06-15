# ha_id: Home Assistant entity ID
class Entity:
    def __init__(self, api, ha_id):
        self.api = api
        self.ha_id = ha_id
        # TODO: FIX ME
        # This will be replaced, AFTER initialisation, super hacky, but it has to be done like this for now. :'(
        self.room = None
