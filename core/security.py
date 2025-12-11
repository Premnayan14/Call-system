# core/security.py

import json


class SecurityController:
    def __init__(self, users_file_path, policy_manager):
        self.users_file_path = users_file_path
        self.policy_manager = policy_manager
        self.users = self._load_users()

    def _load_users(self):
        with open(self.users_file_path, "r") as file:
            return json.load(file)

    def authenticate(self, username, password):
        user = self.users.get(username)

        if user and user["password"] == password:
            role = user["role"]
            permissions = self.policy_manager.get_permissions(role)

            return {
                "username": username,
                "role": role,
                "permissions": permissions,
            }

        return None
