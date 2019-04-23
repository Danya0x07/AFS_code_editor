from tkinter import (Label, Entry, Button, Frame)
from tkinter.constants import *

from serial import Serial, SerialException

from receiver import Receiver
from view import *


class ConnectFrame(Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.port = Serial(timeout=None, interCharTimeout=2)
        self.lbl_port = Label(self, text="Порт: ", font='consolas 11 bold')
        self.lbl_baud = Label(self, text="Скорость: ", font='consolas 11 bold')

        self.entry_port = Entry(self, **entry_port_view)
        self.entry_baud = Entry(self, **entry_baud_view)
        self.btn_connect = Button(self, **btn_connect_view,
                                  command=self.connect)
        self.lbl_connect = Label(self, text=" ", font='consolas 11 bold')

    def pack(self, **kwargs):
        self.lbl_port.grid(row=0, column=0, sticky=W)
        self.entry_port.grid(row=0, column=1)
        self.lbl_baud.grid(row=1, column=0)
        self.entry_baud.grid(row=1, column=1)
        self.btn_connect.grid(row=0, column=2, rowspan=2)
        self.lbl_connect.grid(row=2, columnspan=3)
        super().pack(**kwargs)

    def connect(self, event=None):
        if self.port.is_open:
            return
        try:
            port = self.entry_port.get()
            baud = int(self.entry_baud.get())
            self.port.port = port
            self.port.baudrate = baud
            self.port.open()
            Receiver(self.port).start()
        except SerialException:
            status_text = "Не удалось открыть порт"
            status_color = 'darkred'
        except ValueError:
            status_text = "Некорректные данные"
            status_color = 'darkred'
        else:
            status_text = "Порт открыт"
            status_color = 'darkgreen'
            self.entry_port.config(state='disabled')
            self.entry_baud.config(state='disabled')
            self.btn_connect.configure(text="Отключиться",
                                       command=self.disconnect)
        finally:
            self.lbl_connect['text'] = status_text
            self.lbl_connect['fg'] = status_color
            self.root.after(4000, lambda:
                self.lbl_connect.configure(text=" ", fg='black'))

    def disconnect(self, event=None):
        if self.port.is_open:
            self.port.close()
            self.lbl_connect['text'] = 'Порт закрыт'
            self.lbl_connect['fg'] = 'black'
            self.entry_port.config(state='normal')
            self.entry_baud.config(state='normal')
            self.btn_connect.config(text="Подключиться",
                                       command=self.connect)
            self.root.after(4000, lambda:
                self.lbl_connect.configure(text=" "))

