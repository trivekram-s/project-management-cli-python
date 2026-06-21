"""
models/user.py
Defines the Person base class and User subclass with OOP features.
"""


class Person:
    """Base class representing a generic person with a name."""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    def __repr__(self) -> str:
        return f"Person(name={self._name!r})"


class User(Person):
    """
    Represents a system user who can own projects.
    Inherits from Person and adds email and project tracking.
    """

    _id_counter: int = 1  # Class-level ID counter

    def __init__(self, name: str, email: str, user_id: int = None):
        super().__init__(name)
        self._email = email
        self.user_id = user_id if user_id is not None else User._id_counter
        User._id_counter = max(User._id_counter, self.user_id) + 1
        self.projects: list = []  # List of Project objects owned by this user

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError(f"Invalid email address: {value!r}")
        self._email = value.strip()

    def add_project(self, project) -> None:
        """Associate a Project with this user."""
        self.projects.append(project)

    def to_dict(self) -> dict:
        """Serialize User to a JSON-compatible dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Deserialize a User from a dictionary."""
        return cls(
            name=data["name"],
            email=data["email"],
            user_id=data["user_id"],
        )

    def __str__(self) -> str:
        return f"[User #{self.user_id}] {self.name} <{self.email}>"

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name={self.name!r}, email={self.email!r})"
