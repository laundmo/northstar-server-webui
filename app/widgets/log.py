from typing import Iterable
from lona.html import Widget, Div, Span
from app.northstar.utils import LogMessage


class ReversedContentDiv(Div):
    STYLE = {
        "overflow-y": "auto",
        "display": "flex",
        "flex-direction": "column-reverse",
    }


class LogWidget(Widget):
    def __init__(self, initial_content: Iterable[LogMessage]):
        self.log_area_div = Div(style="white-space: pre-wrap; line-height: 1.2;")
        self.nodes = [
            ReversedContentDiv(
                self.log_area_div,
                style="max-height: 80vh;",
            )
        ]
        for log in initial_content:
            self.add_message(log)

    def add_message(self, msg: LogMessage):
        self.log_area_div.append(Span(msg.message))
