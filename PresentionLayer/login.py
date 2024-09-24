from tkinter import Frame, Label, Entry, Button, messagebox, END
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from BusinessLogicLayer.user_business_logic import UserBusinessLogic


class LoginFrame(ttk.Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.user_business_logic = UserBusinessLogic()

        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="Login Form", bootstyle="info")
        self.header.grid(row=0, column=1, pady=10, padx=10)

        self.username_label = ttk.Label(self, text="Username")
        self.username_label.grid(row=1, column=0, pady=(0, 10), padx=0, sticky="e")

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.password_label = ttk.Label(self, text="Password")
        self.password_label.grid(row=2, column=0, pady=(0, 10), padx=0, sticky="e")

        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.login_button = ttk.Button(self, text="login", command=self.login, bootstyle="success-outline")
        self.login_button.grid(row=3, column=1, pady=(0, 10), padx=0, sticky="w")

        self.sign_up_button = ttk.Button(self, text="Sign Up", command=self.sign_up, bootstyle="primery-outline")
        self.sign_up_button.grid(row=3, column=1, pady=(0, 10), padx=(0, 20), sticky="e")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = self.user_business_logic.login(username, password)

        if not response.success:
            messagebox.showerror("Error", response.message)

        else:
            self.main_view.set_current_user_id(response.data.get_id())
            self.clear_data()
            home_frame = self.main_view.switch_frame("home")
            home_frame.set_current_user(response.data)

    def clear_data(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def sign_up(self):
        self.main_view.switch_frame("sign_up")
