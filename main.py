from tkinter import Tk

from connect_frame import ConnectFrame
from send_frame import SendFrame
from menu import MainMenu


if __name__ == '__main__':
    root = Tk()
    root.title("AFS code editor")
    root.minsize(1000, 825)
    root.geometry("1000x825")

    cf = ConnectFrame(root)
    sf = SendFrame(root, cf.port)

    cf.pack()
    sf.pack(fill='both')

    MainMenu(root, sf.text_editor)

    root.mainloop()
