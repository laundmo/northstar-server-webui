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

    def __iadd__(self, other: str) -> "Command":
        if self.squirrel:
            self._sqscript += dedent(other).strip().split("\n")
        else:
            self._command += dedent(other).strip()
        return self

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
