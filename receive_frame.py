from tkinter import (Text, Checkbutton, Frame,
                     Button, BooleanVar)
from tkinter.constants import *
from threading import Thread

from view import *


class ReceiveFrame(Frame):
    receiving = False

    def __init__(self, root, cf):
        super().__init__(root)
        self.root = root
        self.cf = cf
        self.port = cf.port
        self.receive_thread = None
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.text_receive = Text(self,**text_receive_view)
        self.btn_receive = Button(self, **btn_receive_view,
                                  command=self.toggle_receiving)
        self.btn_clear = Button(self, **btn_clear_view,
                                command=self.clear_buf)
        self.byte_format = BooleanVar()
        self.convert_flag = Checkbutton(self, **convert_flag_view,
                                        variable=self.byte_format)
        self.signed_byte = BooleanVar()
        self.signed_flag = Checkbutton(self, **signed_flag_view,
                                       variable=self.signed_byte)

    def place_widgets(self):
        self.text_receive.grid(row=0, columnspan=3, sticky=W)
        self.btn_receive.grid(row=1, column=0, rowspan=2, sticky=W)
        self.btn_clear.grid(row=1, column=1, rowspan=2, sticky=W)
        self.convert_flag.grid(row=1, column=2, sticky=W)
        self.signed_flag.grid(row=2, column=2, sticky=W)

    def toggle_receiving(self):
        if not ReceiveFrame.receiving:
            ReceiveFrame.receiving = True
            self.receive_thread = Thread(target=self.receive)
            self.convert_flag.configure(state='disabled')
            self.signed_flag.configure(state='disabled')
            self.btn_receive.configure(text="Остановить")
            self.cf.btn_connect.config(state='disabled')
            self.receive_thread.start()
        else:
            ReceiveFrame.receiving = False
            self.receive_thread.join()
            self.convert_flag.configure(state='active')
            self.signed_flag.configure(state='active')
            self.btn_receive.configure(text="Слушать порт")
            self.cf.btn_connect.config(state='normal')

    def receive(self):
        while ReceiveFrame.receiving :
            if self.port.is_open and self.port.in_waiting:
                data = self.port.read()
                if self.byte_format.get():
                    data = ord(data)
                    if self.signed_byte.get():
                        if data > 127: data -= 256
                    data = str(data) + ' '
                else:
                    data = data.decode('ascii', errors='ignore')
                self.text_receive.insert(END, data)
                self.text_receive.see(END)

    def clear_buf(self):
        if self.port.is_open:
            self.port.reset_input_buffer()
        self.text_receive.delete(0.0, END)
