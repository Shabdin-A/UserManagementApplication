from tkinter import Frame, Label, Button, ttk
from ttkbootstrap.constants import *


class HomeFrame(ttk.Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.current_user = None
        self.main_view = main_view
        self.grid_columnconfigure(0, weight=1)

        self.header = ttk.Label(self, text="")
        self.header.grid(row=0, column=0, pady=10, padx=10)

        self.logout_button = ttk.Button(self, text="Logout", command=self.logout, bootstyle="danger")
        self.logout_button.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.edit_user_button = ttk.Button(self, text="Edit User", command=self.edit_user, bootstyle="info")
        self.edit_user_button.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="ew")

    def set_current_user(self, current_user):
        self.current_user = current_user
        self.header.config(text=f"welcome {current_user.get_fullname()}")

        if current_user.is_admin():
            self.user_management_button = ttk.Button(self, text="User Management", command=self.go_user_management, bootstyle="primry")
            self.user_management_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

    def get_current_user_id(self):
        return self.current_user.id if self.current_user else None

    def logout(self):
        self.main_view.switch_frame("login")

    def go_user_management(self):
        if self.current_user.is_admin():
            user_management_frame = self.main_view.switch_frame("user_management")
            user_management_frame.set_current_user(self.current_user)

    def edit_user(self):
        self.main_view.switch_frame("edit_user")
