import asyncio
from typing import List
from app.northstar.command_formatter import Command
from app.northstar.utils import LogMessage


class CommandRunner:
    def __init__(
        self,
        address: str,
        port: int,
        loop: asyncio.AbstractEventLoop,
    ):
        self.address = address
        self.port = port
        self.reader = None
        self.writer = None
        self.loop = loop

    @classmethod
    async def ainit(cls, address: str, port: int):
        return cls(address, port, asyncio.get_event_loop())

    async def connect(self):  # TODO: maybe use connection_context for this?
        self.reader, self.writer = await asyncio.open_connection(
            self.address, self.port
        )

    def run_command(self, command: str, squirrel: bool = False):
        _command = Command(squirrel)
        _command += command
        future = asyncio.run_coroutine_threadsafe(self.run(_command), self.loop)
        result = future.result()
        return result

    async def run(self, command: Command) -> List[LogMessage]:
        while self.writer is None or self.reader is None or self.writer.is_closing():
            try:
                await self.connect()
            except (OSError, ConnectionRefusedError) as e:
                print(e)
        result: List[LogMessage] = []
        try:
            command_formatted = command.get()
            print(command_formatted)
            self.writer.writelines(command_formatted)
            await self.writer.drain()
            try:
                while True:
                    line = await asyncio.wait_for(self.reader.readline(), 0.2)
                    print(line)
                    msg = LogMessage.from_json(line.decode().strip())
                    result.append(msg)
            except asyncio.TimeoutError:
                return result
        except (OSError, ConnectionRefusedError) as e:
            print(e)
            a = await self.run(command)
            return a
        return result
