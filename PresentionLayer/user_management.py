from tkinter import Frame, Label, Button, messagebox, Tk
from tkinter.ttk import Treeview, Combobox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from BusinessLogicLayer.user_business_logic import UserBusinessLogic


class UserManagementFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.item_list = []
        self.current_user = None

        self.main_view = main_view
        self.user_business = UserBusinessLogic()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.header = ttk.Label(self, text="User Management Form", bootstyle="info")
        self.header.grid(row=0, column=0, padx=10, pady=10)

        self.active_button = ttk.Button(self, text="active", command=self.user_active, bootstyle="success")
        self.active_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        self.deactive_button = ttk.Button(self, text="deactive", command=self.user_deactive, bootstyle="danger")
        self.deactive_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

        self.change_role_button = ttk.Button(self, text="change role", command=self.change_role_id, bootstyle="info-outline")
        self.change_role_button.grid(row=1, column=0, padx=1050, pady=(0, 10), sticky="w")

        self.change_role = ttk.Combobox(self, values=["admin", "default user"], state="readonly", bootstyle="info")
        self.change_role.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.back_button = ttk.Button(self, text="back", command=self.back)
        self.back_button.grid(row=1, column=0, padx=(0, 200), pady=(0, 10), sticky="e")

        self.user_table = ttk.Treeview(self, columns=("firstname", "lastname", "username", "status", "admin"))
        self.user_table.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="news")

        self.user_table.heading("#0", text="No")
        self.user_table.heading("#1", text="First Name")
        self.user_table.heading("#2", text="Last Name")
        self.user_table.heading("#3", text="Username")
        self.user_table.heading("#4", text="Status")
        self.user_table.heading("#5", text="Admin")

    def set_current_user(self, current_user):
        self.current_user = current_user
        if self.current_user.is_admin():
            response = self.user_business.get_users(current_user)
            if response.success:
                self.load_data(response.data)
            else:
                messagebox.showerror("Error", response.message)

    def load_data(self, user_list):
        for item in self.item_list:
            self.user_table.delete(item)
        self.item_list.clear()

        row_number = 1
        for user in user_list:
            item = self.user_table.insert("", "end", iid=user.id, text=row_number, values=(
                user.first_name, user.last_name, user.username, "Active" if user.active else "Deactive",
                "Admin" if user.role_id == 1 else "Defult User"))

            self.item_list.append(item)
            row_number += 1

    def user_active(self):
        if self.current_user.is_admin():
            user_ids = self.user_table.selection()
            self.user_business.active_users(self.current_user, user_ids)
            response = self.user_business.get_users(self.current_user)
            self.load_data(response.data)

    def user_deactive(self):
        if self.current_user.is_admin():
            user_ids = self.user_table.selection()
            self.user_business.deactive_users(self.current_user, user_ids)
            response = self.user_business.get_users(self.current_user)
            self.load_data(response.data)



    def change_role_id(self):
        if self.current_user.is_admin():
            selected_user_ids = self.user_table.selection()
            selected_role = self.change_role.get()
            role_id = 1 if selected_role == "admin" else 2
            response = self.user_business.change_role_id(self.current_user, selected_user_ids, role_id)
            if response.success:
                self.load_data(response.data)
                messagebox.showinfo("Success", response.message)
            else:
                messagebox.showerror("Error", response.message)

    def back(self):
        self.main_view.switch_frame("home")
