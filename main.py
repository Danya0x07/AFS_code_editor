from tkinter import Tk

from connect_frame import ConnectFrame
from send_frame import SendFrame


if __name__ == '__main__':
    root = Tk()
    root.title("AFS code editor")
    root.minsize(1000, 700)

    cf = ConnectFrame(root)
    sf = SendFrame(root, cf.port)

    cf.pack()
    sf.pack()

    root.mainloop()
