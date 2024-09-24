class User:
    def __init__(self, id, firstname, lastname, username, password, active, role_id):
        self.id = id
        self.first_name = firstname
        self.last_name = lastname
        self.username = username
        self.password = password
        self.active = True if active == 1 else False
        self.role_id = role_id

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def is_admin(self):
        return self.role_id == 1

    def get_id(self):
        return self.id
