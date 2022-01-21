from enum import Enum
from typing import List, Literal, Union
from lona.html import Widget, Div, Span, Node
from lona.static_files import StyleSheet, Script, SORT_ORDER
import lona_bootstrap_5 as bs

# TODO: https://github.com/lona-web-org/lona-bootstrap-5/pull/3
# class SpinnerType(Enum):
#     grow = "spinner-grow"
#     border = "spinner-border"


# class SpinnerColor(Enum):
#     primary = "text-primary"
#     secondary = "text-secondary"
#     success = "text-success"
#     danger = "text-danger"
#     warning = "text-warning"
#     info = "text-info"
#     light = "text-light"
#     dark = "text-dark"


# class Spinner(bs.Row):
#     CLASS_LIST = []
#     STYLE = {
#         "position": "absolute",
#     }

#     def __init__(self, *, typ: SpinnerType, color: SpinnerColor, **kwargs):
#         if not isinstance(typ, SpinnerType):
#             raise ValueError("typ has to be a SpinnerType")
#         if not isinstance(color, SpinnerColor):
#             raise ValueError("typ has to be a SpinnerColor")
#         super().__init__(**kwargs)
#         self.nodes = [
#             Div(
#                 Span("Loading...", _class="visually-hidden"),
#                 _class=[typ.value, color.value],
#                 _role="status",
#             )
#         ]


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
        Script(
            name="autocomplete_widget",
            path="../static/autocomplete-widget.js",
            url="autocomplete-widget.js",
        ),
    ]

    def __init__(self, **kwargs):
        self.text_field_id = "test"
        self.is_loading = False
        # self.loading_spinner = Spinner(typ=SpinnerType.grow, color=SpinnerColor.danger)
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

    def toggle_loading(self):
        self.is_loading = not self.is_loading
        if self.is_loading:
            self.text_field.disabled = True
            # self.nodes.insert(0, self.loading_spinner)
        else:
            self.text_field.disabled = False
            # self.nodes.remove(self.loading_spinner)
        self.show()


class CommandInputWidget(Widget):
    def __init__(self, **kwargs):
        self.textinp = AutocompleteText(**kwargs, input_delay=0, bubble_up=True)
        self.response = bs.Div()
        self.nodes = [self.textinp, self.response]
        self.previous_commands = []

    def handle_change(self, input_event):
        if input_event.node is self.textinp.text_field:
            print(input_event)
            self.textinp.toggle_loading()
            result = input_event.request.command_sender.run_command(self.textinp.value)  # type: ignore
            print(result)
            self.response.clear()
            for log in result:
                self.response.append(Span(log.message))
            self.previous_commands.append(self.textinp.value)
            self.textinp.autocomplete = self.previous_commands
            self.textinp.value = ""
            self.textinp.toggle_loading()
            print("end")
