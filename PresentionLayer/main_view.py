from PresentionLayer.window import Window
from PresentionLayer.login import LoginFrame
from PresentionLayer.home import HomeFrame
from PresentionLayer.user_management import UserManagementFrame
from PresentionLayer.sign_up import SingUpFrame
from PresentionLayer.edit_user import EditUser


class MainView:
    def __init__(self):
        self.frames = {}
        self.current_user_id = None

        window = Window()

        self.add_frame("edit_user", EditUser(self, window))
        self.add_frame("sign_up", SingUpFrame(self, window))
        self.add_frame("user_management", UserManagementFrame(self, window))
        self.add_frame("home", HomeFrame(self, window))
        self.add_frame("login", LoginFrame(self, window))

        window.show_form()

    def add_frame(self, name, frame):
        self.frames[name] = frame
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        return frame

    def set_current_user_id(self, user_id):
        self.current_user_id = user_id

    def get_current_user_id(self):
        return self.current_user_id

