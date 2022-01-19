from app.widgets.input import CommandInputWidget
from app.widgets.log import LogWidget
from lona import LonaView
from lona.html import HTML, Tr, Td, Table


class LogView(LonaView):
    def handle_request(self, request):
        self.log_area = LogWidget(initial_content=request.log_queue.old_messages)
        self.input_area = CommandInputWidget(rows=5)
        html = HTML(
            Table(
                Tr(Td(self.log_area)),
                Tr(Td(self.input_area)),
            )
        )
        try:
            with request.log_queue(self.log_area.add_message):
                while True:
                    self.show(html)
                    self.ping()
        except Exception as e:
            print(e)