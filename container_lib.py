import json


class Container:
    def __init__(self, attrs):
        self.id = attrs['Id']
        self.is_running = attrs['State']['Running']

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)