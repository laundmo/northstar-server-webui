import asyncio
from contextlib import asynccontextmanager
from models import BroadcastQueue, LogMessage

log_queue = BroadcastQueue()


@asynccontextmanager
async def connection_context(address: str, port: int):
    reader, writer = await asyncio.open_connection(address, port)
    try:
        yield reader, writer
    finally:
        writer.close()


async def recieve_logs():
    q = log_queue._unread_queue.async_q
    while True:
        async with connection_context("localhost", 9998) as (reader, writer):
            while line := await reader.readline():
                msg = LogMessage.from_json(line.decode().strip())
                await q.put(msg)
