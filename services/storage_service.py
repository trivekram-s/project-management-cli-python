"""
services/storage_service.py
Handles all file I/O for persisting users, projects, and tasks via JSON.
"""

import json
import os
from models.user import User
from models.project import Project

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "project_data.json")


class StorageService:
    """
    Manages loading and saving of all application data to a local JSON file.
    Handles missing files and malformed data gracefully.
    """

    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def load(self) -> dict[str, User]:
        """
        Load all users (and their projects/tasks) from the JSON data file.
        Returns a dict mapping user name (lowercase) -> User object.
        """
        users: dict[str, User] = {}
        if not os.path.exists(self.filepath):
            return users

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)

            for user_data in raw.get("users", []):
                user = User.from_dict(user_data)
                for project_data in user_data.get("projects", []):
                    project = Project.from_dict(project_data)
                    user.add_project(project)
                users[user.name.lower()] = user

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[Storage Warning] Could not fully load data: {e}")

        return users

    def save(self, users: dict[str, User]) -> None:
        """
        Save all users (and their projects/tasks) to the JSON data file.
        """
        try:
            payload = {
                "users": []
            }
            for user in users.values():
                user_dict = user.to_dict()
                user_dict["projects"] = [p.to_dict() for p in user.projects]
                payload["users"].append(user_dict)

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

        except (OSError, TypeError) as e:
            print(f"[Storage Error] Failed to save data: {e}")
