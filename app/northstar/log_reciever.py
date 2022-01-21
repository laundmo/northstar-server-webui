from app.northstar.utils import LogMessage
from app.northstar.utils import connection_context


async def recieve_logs(log_queue):
    q = log_queue._unread_queue.async_q
    while True:
        try:
            async with connection_context("localhost", 9998) as (reader, writer):
                while line := await reader.readline():
                    msg = LogMessage.from_json(line.decode().strip())
                    await q.put(msg)
        except OSError as e:
            print("Log Recieve:", e)