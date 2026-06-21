"""
models/project.py
Defines the Project class with task management and serialization.
"""

from datetime import datetime
from models.task import Task


class Project:
    """
    Represents a project owned by a user, containing multiple tasks.
    Supports one-to-many relationship with Task objects.
    """

    _id_counter: int = 1

    def __init__(
        self,
        title: str,
        owner_name: str,
        description: str = "",
        due_date: str = None,
        created_at: str = None,
        project_id: int = None,
    ):
        self._title = title
        self.owner_name = owner_name
        self._description = description
        self.due_date = due_date or "No due date set"
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.project_id = project_id if project_id is not None else Project._id_counter
        Project._id_counter = max(Project._id_counter, self.project_id) + 1
        self.tasks: list[Task] = []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value.strip() if value else ""

    def add_task(self, task: Task) -> None:
        """Add a Task to this project."""
        self.tasks.append(task)

    def get_task_by_title(self, title: str) -> Task | None:
        """Find a task by title (case-insensitive)."""
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def completion_summary(self) -> dict:
        """Return a dict with task count and completion stats."""
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.status == "complete")
        in_prog = sum(1 for t in self.tasks if t.status == "in-progress")
        pending = sum(1 for t in self.tasks if t.status == "pending")
        return {
            "total": total,
            "complete": done,
            "in_progress": in_prog,
            "pending": pending,
            "percent_done": round((done / total) * 100, 1) if total else 0,
        }

    def to_dict(self) -> dict:
        """Serialize Project to a JSON-compatible dictionary."""
        return {
            "project_id": self.project_id,
            "title": self.title,
            "owner_name": self.owner_name,
            "description": self.description,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Deserialize a Project (and its tasks) from a dictionary."""
        project = cls(
            title=data["title"],
            owner_name=data["owner_name"],
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            created_at=data.get("created_at"),
            project_id=data["project_id"],
        )
        for task_data in data.get("tasks", []):
            project.tasks.append(Task.from_dict(task_data))
        return project

    def __str__(self) -> str:
        stats = self.completion_summary()
        return (
            f"[Project #{self.project_id}] {self.title}\n"
            f"  Owner: {self.owner_name} | Due: {self.due_date}\n"
            f"  Description: {self.description or 'N/A'}\n"
            f"  Tasks: {stats['total']} total | {stats['complete']} done | "
            f"{stats['in_progress']} in-progress | {stats['pending']} pending "
            f"({stats['percent_done']}% complete)"
        )

    def __repr__(self) -> str:
        return f"Project(id={self.project_id}, title={self.title!r}, owner={self.owner_name!r})"
