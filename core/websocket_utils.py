import hashlib
import json
import asyncio


class State:
    def __init__(self):
        self.last_data = None
        self.changed_queue = asyncio.Queue()

    async def notify_changed(self):
        await self.changed_queue.put(True)


def get_data_hash(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
