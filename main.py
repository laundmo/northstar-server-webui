import os
from typing import Iterable
from lona.html import Span, HTML, Div, Tr, Td, Table, TextArea, Widget
from lona import LonaView, LonaApp
from lona.protocol import INPUT_EVENT_TYPE
from models import LogMessage
from log_source import log_queue, start as start_log_source

import lona_bootstrap_5 as bs

app = LonaApp(__file__)


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


class CommandInputWidget(Widget):
    def __init__(self, **kwargs):
        self.textinp = bs.TextInput(**kwargs, input_delay=0, bubble_up=True)
        self.nodes = [self.textinp]

    def handle_input_event(self, input_event):
        if input_event.node is self.textinp:
            if input_event.type == INPUT_EVENT_TYPE.CHANGE:
                print(input_event.data)
                self.textinp.value = ""


@app.route("/")
class LogView(LonaView):
    def handle_request(self, request):
        self.log_area = LogWidget(initial_content=log_queue.old_messages)
        self.input_area = CommandInputWidget(rows=5)
        html = HTML(
            Table(
                Tr(Td(self.log_area)),
                Tr(Td(self.input_area)),
            )
        )
        with log_queue(self.log_area.add_message):
            while True:
                self.show(html)
                self.sleep(0.1)


if __name__ == "__main__":
    with start_log_source():
        app.run(port=8080)
    # os._exit(0)
