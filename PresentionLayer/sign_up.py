from tkinter import Frame, Label, Entry, Button, messagebox, ttk
from ttkbootstrap import *
from BusinessLogicLayer.user_business_logic import UserBusinessLogic


class SingUpFrame(ttk.Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.user_business_logic = UserBusinessLogic()

        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="Sign Up Form", bootstyle="info")
        self.header.grid(row=0, column=1, padx=0, pady=(0, 10))

        self.first_name = ttk.Label(self, text="First Name")
        self.first_name.grid(row=1, column=0, padx=0, pady=(0, 10), sticky='e')

        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(row=1, column=1, padx=(0, 20), pady=(0, 10), sticky='ew')

        self.last_name = ttk.Label(self, text="Last Name")
        self.last_name.grid(row=2, column=0, padx=0, pady=(0, 10), sticky='e')

        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(row=2, column=1, padx=(0, 20), pady=(0, 10), sticky='ew')

        self.username_label = ttk.Label(self, text="Username")
        self.username_label.grid(row=3, column=0, padx=0, pady=(0, 10), sticky='e')

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=3, column=1, padx=(0, 20), pady=(0, 10), sticky='ew')

        self.password_label = ttk.Label(self, text="Password")
        self.password_label.grid(row=4, column=0, padx=0, pady=(0, 10), sticky='e')

        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(row=4, column=1, padx=(0, 20), pady=(0, 10), sticky='ew')

        self.sign_up_button = ttk.Button(self, text="sign up", command=self.sign_up, bootstyle="success-outline")
        self.sign_up_button.grid(row=5, column=1, padx=0, pady=(0, 10), sticky='w')

        self.back_button = ttk.Button(self, text="back", command=self.back, bootstyle="primary-outline")
        self.back_button.grid(row=5, column=1, padx=(0, 10), pady=(0, 10), sticky='e')

    def sign_up(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = self.user_business_logic.sign_up(first_name, last_name, username, password)
        if response.success:
            messagebox.showinfo("Success", response.message)
            self.main_view.switch_frame("login")
        else:
            messagebox.showerror("Error", response.message)

    def back(self):
        self.main_view.switch_frame("login")
