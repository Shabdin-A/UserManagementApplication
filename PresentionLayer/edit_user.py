from tkinter import Frame, Label, Entry, Button, messagebox, ttk
from ttkbootstrap import *
from BusinessLogicLayer.user_business_logic import UserBusinessLogic


class EditUser(ttk.Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.user_business_logic = UserBusinessLogic()

        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="Edit User", bootstyle="info")
        self.header.grid(row=0, column=1, padx=10, pady=10)

        self.first_name = ttk.Label(self, text="First Name")
        self.first_name.grid(row=1, column=0, padx=0, pady=(0, 10), sticky='w')

        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=(0, 20), sticky='ew')

        self.last_name = ttk.Label(self, text="Last Name")
        self.last_name.grid(row=2, column=0, padx=0, pady=(0, 10), sticky='w')

        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(row=2, column=1, padx=10, pady=(0, 20), sticky='ew')

        self.username = ttk.Label(self, text="Username")
        self.username.grid(row=3, column=0, padx=0, pady=(0, 10), sticky='w')

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=3, column=1, padx=10, pady=(0, 20), sticky='ew')

        self.current_password = ttk.Label(self, text="Current Password")
        self.current_password.grid(row=4, column=0, padx=10, pady=(0, 10), sticky='w')

        self.current_password_entry = ttk.Entry(self)
        self.current_password_entry.grid(row=4, column=1, padx=10, pady=(0, 20), sticky='ew')

        self.new_password = ttk.Label(self, text="New Password")
        self.new_password.grid(row=5, column=0, padx=10, pady=(0, 10), sticky='w')

        self.new_password_entry = ttk.Entry(self)
        self.new_password_entry.grid(row=5, column=1, padx=10, pady=(0, 20), sticky='ew')

        self.confirm_new_password = ttk.Label(self, text="Confirm New Password")
        self.confirm_new_password.grid(row=6, column=0, padx=10, pady=(0, 10), sticky='w')

        self.confirm_new_password_entry = ttk.Entry(self)
        self.confirm_new_password_entry.grid(row=6, column=1, padx=10, pady=(0, 20), sticky='ew')

        self.change_button = ttk.Button(self, text="Submit", command=self.change_user_info, bootstyle="success-outline")
        self.change_button.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        self.back_button = ttk.Button(self, text="back", command=self.back, bootstyle="primary-outline")
        self.back_button.grid(row=7, column=1, padx=10, pady=(0, 10), sticky="e")

    def load_user_info(self, user_id):
        response = self.user_business_logic.get_user_info(user_id)
        if response.success:
            user_data = response.data
            self.first_name_entry.delete(0, "end")
            self.first_name_entry.insert(0, user_data.first_name)
            self.last_name_entry.delete(0, "end")
            self.last_name_entry.insert(0, user_data.last_name)
            self.username_entry.delete(0, "end")
            self.username_entry.insert(0, user_data.username)

        else:
            messagebox.showerror("Error", response.message)

    def change_user_info(self):
        user_id = self.main_view.get_current_user_id()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_new_password = self.confirm_new_password_entry.get()

        response = self.user_business_logic.update_user_info(user_id, first_name, last_name, username, new_password)
        if response.success:
            password_change_response = self.user_business_logic.change_password(user_id, current_password, new_password,
                                                                                confirm_new_password)
            if password_change_response.success:
                messagebox.showinfo("Success", "User information and password updated successfully")
            else:
                messagebox.showerror("Error", password_change_response.message)
        else:
            messagebox.showerror("Error", response.message)


    def back(self):
        self.main_view.switch_frame("home")
