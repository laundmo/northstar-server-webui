import asyncio
from app.northstar.command_sender import CommandRunner
from app.northstar.utils import BroadcastQueue

from app.northstar.log_reciever import recieve_logs


class SocketStart:
    def __init__(self):
        self.log_queue: BroadcastQueue = None  # type: ignore
        self.command_sender: CommandRunner = None  # type: ignore

    async def on_startup(self, data):
        self.command_sender = await CommandRunner.ainit("localhost", 9999)
        self.log_queue = await BroadcastQueue.ainit()
        self.log_queue.start()
        self.logs_task = asyncio.create_task(recieve_logs(self.log_queue))

        return data

    async def on_shutdown(self, data):
        # server = data.server
        # TODO: close sockets and stop BroadcastQueue
        return data

    def handle_request(self, data):
        request = data.request
        request.log_queue = self.log_queue
        request.command_sender = self.command_sender
        return data
