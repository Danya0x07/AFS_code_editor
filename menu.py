from tkinter import Menu
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.constants import END


class MainMenu(Menu):
    def __init__(self, root, txt_editor):
        super().__init__(root)
        self.txt_editor = txt_editor
        file_menu = Menu(self, tearoff=False)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        self.add_cascade(label="Файл", menu=file_menu)
        root.configure(menu=self)

    def open_file(self):
        fname = askopenfilename()
        if not fname: return
        with open(fname, 'r') as f:
            self.txt_editor.delete(1.0, END)
            self.txt_editor.insert(END, f.read())

    def save_file(self):
        fname = asksaveasfilename()
        if not fname: return
        text = self.txt_editor.get(1.0, END)
        with open(fname, 'w') as f:
            f.write(text)
