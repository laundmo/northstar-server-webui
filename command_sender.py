import asyncio
from textwrap import dedent


class Command:
    def __init__(self, squirrel: bool):
        self._squirrel = squirrel
        self._command = ""
        self._sqscript = []
        self.result = ""

    @property
    def squirrel(self):
        return self._squirrel

    @squirrel.setter
    def _(self, value: bool):
        if self._squirrel == value:
            return
        if self._command == "" and len(self._sqscript) == 0:
            self._squirrel = value
        else:
            raise ValueError("Command already contains content, cannot change type.")

    @property
    def command(self):
        return self._command

    @command.setter
    def _(self, value: str):
        if self._command == "" and not self.squirrel:
            self._command = value
        else:
            raise ValueError("Command is a squirrel command.")

    def __iadd__(self, other: str):
        if self.squirrel:
            self._sqscript += dedent(other).strip().split("\n")

    def __str__(self) -> str:
        if self.squirrel:
            return (
                f"<Command(squirrel) [{self._sqscript[0]}, ..., {self._sqscript[-1]}]>"
            )
        else:
            return f"<Command(console) {self._command}>"

    def get(self):
        if self.squirrel:
            return [s.encode() + b"\n" for s in ["BOF"] + self._sqscript + ["EOF"]]
        else:
            return [self._command.encode() + b"\n"]


class RunCommandCtx:
    def __init__(self, sqirrel: bool, client: "SocketCommandClient"):
        self.sqirrel = sqirrel
        self.client = client

    async def __aenter__(self):
        self.command = Command(self.sqirrel)
        return self.command

    async def __aexit__(self, *args):
        result = await self.client.run(self.command)
        self.command.result = result


class SocketCommandClient:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.result = ""

    @classmethod
    async def ainit(cls, address: str, port: int):
        reader, writer = await asyncio.open_connection(address, port)
        return cls(reader, writer)

    def __call__(self, squirrel: bool):
        return RunCommandCtx(squirrel, self)

    async def run(self, command: Command):
        self.writer.writelines(command.get())
        await self.writer.drain()
        self.result = ""
        try:
            while True:
                buf = await asyncio.wait_for(self.reader.readline(), 0.05)
                self.result += buf.decode(errors="replace")
        except asyncio.TimeoutError:
            return self.result


async def main():
    c = await SocketCommandClient.ainit("localhost", 9999)
    with open("func.txt") as f:
        # with open("out.txt", "w+") as f2:
        for line in f:
            async with c(True) as command:
                command += f"""
                    typeof {line.strip()};
                    """
            print(
                [line for line in c.result.split("\n") if "SERVER SCRIPT" in line][0]
                + "\n"
            )


# async def main():
#     c = await SocketCommandClient.ainit("localhost", 9999)

#     async with c(True) as command:
#         command += """
#     foreach (key, value in getroottable()){
#         print(key);
#     }"""
#     print(c.result)
#     await asyncio.sleep(5)


asyncio.run(main())
