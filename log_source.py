import socket
import threading
import time
from contextlib import contextmanager
from models import BroadcastQueue, LogMessage

log_queue = BroadcastQueue()


class LogConsumer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect(("localhost", 9998))
                    # TODO: infinite reconnects for some reason ?
                    print("Connection to server established")
                except ConnectionRefusedError:
                    time.sleep(0.1)
                    print("Connection refused")
                    continue
                try:
                    while True:
                        if self.shutdown_flag.is_set():
                            return
                        data = ""

                        while "\n" not in data:
                            if self.shutdown_flag.is_set():
                                return
                            data += s.recv(1).decode()

                        msg = LogMessage.from_json(data[:-1])
                        log_queue.put(msg)
                except (ConnectionResetError, OSError) as e:
                    time.sleep(0.1)
                    print("Connection lost while recieving data", e)


@contextmanager
def start():
    lc = LogConsumer()
    lc.start()
    log_queue.start()
    try:
        yield None
    finally:
        lc.shutdown_flag.set()
        lc.join()
