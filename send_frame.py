from tkinter import (Entry, Checkbutton, Button,
                     BooleanVar, Label, Frame, Text)
from tkinter.constants import *

from serial import SerialException

from view import *


class SendFrame(Frame):

    def __init__(self, root, port):
        super().__init__(root)
        self.root = root
        self.port = port
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.entry_send = Entry(self, **entry_send_view)
        self.btn_line_send = Button(self, **btn_line_send_view,
                               command=self.send_line_msg)
        self.text_send = Text(self, **text_send_view)
        self.btn_text_send = Button(self, **btn_text_send_view,
                                    command=self.send_text_msg)
        self.lbl_status_send = Label(self, text=" ")

    def place_widgets(self):
        self.entry_send.grid(columnspan=2, sticky=W)
        self.btn_line_send.grid(row=0, column=2, sticky=W)
        self.text_send.grid(row=1, column=0, sticky=W)
        self.btn_text_send.grid(row=2, column=1)
        self.lbl_status_send.grid(row=2, columnspan=2)

    def send_line_msg(self, event=None):
        msg = self.entry_send.get()
        try:
            msg += '\r\n'
            msg = bytes(msg, 'ascii')
            self.port.write(msg)
        except UnicodeDecodeError:
            self._show_status_msg("Некорректный ввод", "darkred")
        except SerialException:
            self._show_status_msg("Ошибка отправки", "darkred")
        else:
            self.entry_send.delete(0, END)

    def send_text_msg(self, event=None):
        code = self.text_send.get(0.0, END).split('\n')
        program = self._compile_code(code)
        if program is None: return
        for byte_line in program:
            self._send_byte_line(byte_line)

    def _show_status_msg(self, error_text, color):
        self.lbl_status_send.configure(text=error_text, fg=color)
        self.root.after(4000, lambda:
            self.lbl_status_send.configure(text=" ", fg='black'))

    def _compile_code(self, code):
        program = []
        for line in code:
            line = line.replace('\n', '\r\n')
            try:
                msg = bytes(line, 'ascii')
            except UnicodeDecodeError:
                error_msg = "Некорректный ввод, строка {}".format(line)
                self._show_status_msg(error_msg, "darkred")
                return None
            else:
               program.append(msg)
        return program

    def _send_byte_line(self, byte_line):
        try:
            self.port.write(byte_line)
        except SerialException:
            self._show_status_msg("Ошибка отправки", "darkred")


