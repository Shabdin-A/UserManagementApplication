from tkinter import Tk
import ttkbootstrap as ttk


class Window(ttk.Window):
    def __init__(self):
        # journal
        super().__init__(themename="solar")

        self.title("User Management Application")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.geometry("1000x900")

    def show_form(self):
        self.mainloop()
