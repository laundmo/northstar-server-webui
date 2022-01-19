import asyncio
from contextlib import asynccontextmanager
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
import json
from typing import Callable, Dict
import dataclass_factory
import threading
import janus


class MessageTypes(Enum):
    log = "log"


factory = dataclass_factory.Factory()


@dataclass
class LogMessage:
    message: str
    typ: MessageTypes

    @classmethod
    def from_json(cls, json_str: str):
        return factory.load(json.loads(json_str), cls)


@contextmanager
def queue_subscription(queue: "BroadcastQueue", callback: Callable[[LogMessage], None]):
    queue.register_notify(callback)
    try:
        yield queue
    finally:
        queue.unregister_notify(callback)


class BroadcastQueue(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.old_messages: "deque[LogMessage]" = deque(maxlen=3000)
        self.notify: Dict[int, Callable[[LogMessage], None]] = {}
        self._unread_queue: janus.Queue[LogMessage] = None  # type: ignore
        self.unread_queue: janus.SyncQueue[LogMessage] = None  # type: ignore

    @classmethod
    async def ainit(cls):
        ins = cls()
        ins._unread_queue = janus.Queue()
        ins.unread_queue = ins._unread_queue.sync_q
        return ins

    def __call__(self, callback: Callable[[LogMessage], None]):
        return queue_subscription(self, callback)

    def put(self, message):
        self.unread_queue.put(message)

    def put_nowait(self, message):
        self.unread_queue.put_nowait(message)

    def register_notify(self, callback: Callable[[LogMessage], None]):
        self.notify[id(callback)] = callback

    def unregister_notify(self, callback: Callable[[LogMessage], None]):
        del self.notify[id(callback)]

    def run(self):
        while True:
            msg = self.unread_queue.get()
            for callback in self.notify.values():
                callback(msg)
            self.old_messages.appendleft(msg)


@asynccontextmanager
async def connection_context(address: str, port: int):
    reader, writer = await asyncio.open_connection(address, port)
    try:
        yield reader, writer
    finally:
        writer.close()
