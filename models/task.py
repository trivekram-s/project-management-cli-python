"""
models/task.py
Defines the Task class with status management and serialization.
"""

from datetime import datetime


VALID_STATUSES = ("pending", "in-progress", "complete")


class Task:
    """
    Represents a task assigned to a project.
    Supports status transitions and optional contributor assignment.
    """

    _id_counter: int = 1

    def __init__(
        self,
        title: str,
        assigned_to: str = "Unassigned",
        status: str = "pending",
        created_at: str = None,
        task_id: int = None,
    ):
        self._title = title
        self._status = status
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.task_id = task_id if task_id is not None else Task._id_counter
        Task._id_counter = max(Task._id_counter, self.task_id) + 1

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {VALID_STATUSES}")
        self._status = value

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self._status = "complete"

    def mark_in_progress(self) -> None:
        """Mark this task as in-progress."""
        self._status = "in-progress"

    def to_dict(self) -> dict:
        """Serialize Task to a JSON-compatible dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize a Task from a dictionary."""
        return cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", "Unassigned"),
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            task_id=data["task_id"],
        )

    def __str__(self) -> str:
        icon = "✅" if self.status == "complete" else ("🔄" if self.status == "in-progress" else "⏳")
        return f"  {icon} [{self.task_id}] {self.title} (assigned: {self.assigned_to}, status: {self.status})"

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, title={self.title!r}, status={self.status!r})"
