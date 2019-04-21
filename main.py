from tkinter import Tk
from tkinter.constants import *

from connect_frame import ConnectFrame
from send_frame import SendFrame
from receiver import Receiver


if __name__ == '__main__':
    root = Tk()
    root.title("AFM code editor")
    root.minsize(1000, 700)

    cf = ConnectFrame(root)
    sf = SendFrame(root, cf.port)
    #rf = ReceiveFrame(root, cf)

    cf.pack()
    sf.pack()

    #rf.pack(side=RIGHT)

    root.mainloop()
