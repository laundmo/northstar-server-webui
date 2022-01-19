from typing import List
from lona.html import Widget, Div, Span
from lona.static_files import StyleSheet, Script, SORT_ORDER
import lona_bootstrap_5 as bs


class AutocompleteText(Widget):
    FRONTEND_WIDGET_CLASS = "AutocompleteTextWidget"
    STATIC_FILES = [
        StyleSheet(
            name="jquery_ui_css",
            path="../static/jquery-ui.css",
            url="jquery-ui.css",
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        Script(
            name="jquery_min_js",
            path="../static/jquery.min.js",
            url="jquery.min.js",
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        Script(
            name="jquery_ui_js",
            path="../static/jquery-ui.js",
            url="jquery-ui.js",
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        Script(name="autocomplete_widget", path="../static/autocomplete-widget.js"),
    ]

    def __init__(self, **kwargs):
        self.text_field_id = "test"
        self.text_field = bs.TextInput(_id=self.text_field_id, **kwargs)
        self.nodes = [Div(self.text_field, _class="ui-widget")]
        self.data = ["#" + self.text_field_id, []]
        # TODO: how to bubble up input events?

    @property
    def autocomplete(self):
        return self.data[1]

    @autocomplete.setter
    def autocomplete(self, autocomplete: List[str]):
        self.data = ["#" + self.text_field_id, autocomplete]

    @property
    def value(self):
        return self.text_field.value

    @value.setter
    def value(self, value: str):
        self.text_field.value = value


class CommandInputWidget(Widget):
    def __init__(self, **kwargs):
        self.textinp = AutocompleteText(**kwargs, input_delay=0, bubble_up=True)
        self.response = bs.Div()
        self.nodes = [self.textinp, self.response]
        self.previous_commands = []

    def handle_change(self, input_event):
        if input_event.node is self.textinp.text_field:
            print(input_event)
            # result = command_sender.run_command(self.textinp.value)  # type: ignore # TODO: this wont work until i can pass the command_sender in here somehow. but how?
            # print(result)
            # self.response.clear()
            # for log in result:
            #     self.response.append(Span(log.message))
            self.previous_commands.append(self.textinp.value)
            self.textinp.autocomplete = self.previous_commands
            self.textinp.value = ""
            print("end")
