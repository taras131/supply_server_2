import hashlib
import json


class State:
    def __init__(self):
        self.last_data = None
        self.changed = False


def get_data_hash(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
