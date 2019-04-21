from threading import Thread
from serial import SerialException


class Receiver(Thread):
    def __init__(self, port):
        super().__init__(daemon=False)
        self.port = port

    def run(self):
        while self.port.is_open:
            try:
                if self.port.in_waiting:
                    data = self.port.read()
                    data = data.decode('ascii', errors='ignore')
                    print(data, end='')
            except SerialException:
                break

