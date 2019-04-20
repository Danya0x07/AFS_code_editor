from tkinter import Tk
from tkinter.constants import *

from connect_frame import ConnectFrame
from send_frame import SendFrame


if __name__ == '__main__':
    root = Tk()
    root.title("AFM code editor")
    root.minsize(1000, 600)

    cf = ConnectFrame(root)
    sf = SendFrame(root, cf.port)

    cf.pack(anchor=NW)
    sf.pack(anchor=NW)

    root.mainloop()
