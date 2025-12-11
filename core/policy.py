# core/policy.py

import json


class PolicyManager:
    def __init__(self, policy_file_path):
        self.policy_file_path = policy_file_path
        self.policy_data = self._load_policy()

    def _load_policy(self):
        with open(self.policy_file_path, "r") as file:
            return json.load(file)

    def get_permissions(self, role):
        return self.policy_data.get(role, [])
