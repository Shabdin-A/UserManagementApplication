import hashlib
from Common.response import Response
from Common.user import User
from DataAccessLayer.user_data_access import UserDataAccess
from Common.performance_logger import performance_logger


class UserBusinessLogic:
    def __init__(self):
        self.user_data_access = UserDataAccess()

    @performance_logger(1)
    def login(self, username, password):
        if len(username) < 3 or len(password) < 6:
            return Response(None, "Invalid Data", False)

        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        user = self.user_data_access.get_user(username, hashed_password)

        if user:
            if user.active:
                return Response(user, "Login Successful", True)
            else:
                return Response(None, "your account is not active", False)
        else:
            return Response(None, "Invalid username or password", False)

    @performance_logger(1)
    def get_users(self, current_user):
        if not current_user.is_admin():
            return Response(None, "Invalid Access", False)
        if not current_user.active:
            return Response(None, "Your account is not active", False)

        user_list = self.user_data_access.get_users(current_user.id)
        return Response(user_list, "Login Successful", True)

    @performance_logger(3)
    def active_users(self, current_user, ids):
        if not current_user.is_admin():
            return Response(None, "Invalid Access", False)
        for id in ids:
            self.user_data_access.update_active(id, 1)

    @performance_logger(3)
    def deactive_users(self, current_user, ids):
        if not current_user.is_admin():
            return Response(None, "Invalid Access", False)
        for id in ids:
            self.user_data_access.update_active(id, 0)

    @performance_logger(2)
    def sign_up(self, first_name, last_name, username, password):
        if len(username) < 3 or len(password) < 6:
            return Response(None, "Invalid Data", False)

        sign_user = self.user_data_access.get_user_by_username(username)
        if sign_user:
            return Response(None, "Username already exists", False)

        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        self.user_data_access.new_user(first_name, last_name, username, hashed_password)
        return Response(None, "Sign Up Successful, please wait for admin approval", True)

    @performance_logger(3)
    def change_role_id(self, current_user, user_ids, role_id):
        if not current_user.is_admin():
            return Response(None, "Invalid Access", False)

        for user_id in user_ids:
            self.user_data_access.change_role_id(user_id, role_id)

        user_list = self.user_data_access.get_users(current_user.id)
        return Response(user_list, "Role updated successfully", True)

    def get_user_info(self, user_id):
        user_info = self.user_data_access.get_user_info(user_id)
        if user_info:
            user = User(
                id=user_info["id"],
                firstname=user_info["first_name"],
                lastname=user_info["last_name"],
                username=user_info["username"],
                password=user_info["password"]
            )
            return Response(user, "User data retrieved successfully", True)
        else:
            return Response(None, "User not found", False)

    @performance_logger(3)
    def update_user_info(self, user_id, first_name, last_name, username, password):
        hashed_password = self.user_data_access.hash_password(password)
        if user_id and user_id > 0:
            success = self.user_data_access.update_user_info(user_id, first_name, last_name, username, hashed_password)
            if success:
                return Response(None, "User updated successfully", True)
            else:
                return Response(None, "Failed to update user", False)
        return Response(None, "Invalid user ID", False)



    @performance_logger(3)
    def change_password(self, user_id, current_password, new_password, confirm_new_password):
        if new_password != confirm_new_password:
            return Response(None, "New passwords do not match", False)

        if not self.user_data_access.check_current_password(user_id, current_password):
            return Response(None, "Current password is incorrect", False)

        if self.user_data_access.update_password(user_id, new_password):
            return Response(None, "Password changed successfully", True)
        else:
            return Response(None, "Failed to change password", False)

