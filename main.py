"""
main.py
CLI entry point for the Project Management Tool.
Uses argparse for subcommands; delegates logic to models and services.

Usage:
    python main.py <command> [options]

Commands:
    add-user        Add a new user
    list-users      List all users
    add-project     Add a project to a user
    list-projects   List all projects for a user
    add-task        Add a task to a project
    list-tasks      List all tasks for a project
    complete-task   Mark a task as complete
    start-task      Mark a task as in-progress
    summarize-project  Generate an AI summary of a project
    suggest-next    Get an AI next-step suggestion for a project
"""

import argparse
import sys

from models.user import User
from models.project import Project
from models.task import Task
from services.storage_service import StorageService
from services.ai_client import AIClient
from utils.formatters import (
    print_success,
    print_error,
    print_info,
    print_users_table,
    print_projects_table,
    print_tasks_table,
    print_ai_panel,
)

# ── Initialise shared services ────────────────────────────────────────────────
storage = StorageService()
ai_client = AIClient()


# ── Helper look-ups ───────────────────────────────────────────────────────────

def _get_user(users: dict, name: str):
    """Return a User by name (case-insensitive) or print an error and exit."""
    user = users.get(name.lower())
    if not user:
        print_error(f"User '{name}' not found. Use 'list-users' to see all users.")
        sys.exit(1)
    return user


def _get_project(user, title: str):
    """Return a Project from a user by title (case-insensitive) or exit."""
    for project in user.projects:
        if project.title.lower() == title.lower():
            return project
    print_error(
        f"Project '{title}' not found for user '{user.name}'. "
        "Use 'list-projects' to see all projects."
    )
    sys.exit(1)


# ── Command handlers ──────────────────────────────────────────────────────────

def cmd_add_user(args, users: dict) -> None:
    """Create and persist a new user."""
    if args.name.lower() in users:
        print_error(f"A user named '{args.name}' already exists.")
        return
    user = User(name=args.name, email=args.email)
    users[user.name.lower()] = user
    storage.save(users)
    print_success(f"User created: {user}")


def cmd_list_users(args, users: dict) -> None:
    """Display all users in a table."""
    print_users_table(users)


def cmd_add_project(args, users: dict) -> None:
    """Create a project and add it to a user."""
    user = _get_user(users, args.user)
    # Check for duplicate project title under this user
    for p in user.projects:
        if p.title.lower() == args.title.lower():
            print_error(f"Project '{args.title}' already exists for '{user.name}'.")
            return
    project = Project(
        title=args.title,
        owner_name=user.name,
        description=args.description or "",
        due_date=args.due_date or "No due date set",
    )
    user.add_project(project)
    storage.save(users)
    print_success(f"Project '{project.title}' added to user '{user.name}'.")


def cmd_list_projects(args, users: dict) -> None:
    """List all projects for a user."""
    user = _get_user(users, args.user)
    print_projects_table(user)


def cmd_add_task(args, users: dict) -> None:
    """Add a task to a project."""
    user = _get_user(users, args.user)
    project = _get_project(user, args.project)
    # Check duplicate task title
    if project.get_task_by_title(args.title):
        print_error(f"Task '{args.title}' already exists in project '{project.title}'.")
        return
    task = Task(title=args.title, assigned_to=args.assigned_to or "Unassigned")
    project.add_task(task)
    storage.save(users)
    print_success(f"Task '{task.title}' added to project '{project.title}'.")


def cmd_list_tasks(args, users: dict) -> None:
    """List all tasks for a project."""
    user = _get_user(users, args.user)
    project = _get_project(user, args.project)
    print_tasks_table(project)


def cmd_complete_task(args, users: dict) -> None:
    """Mark a task as complete."""
    user = _get_user(users, args.user)
    project = _get_project(user, args.project)
    task = project.get_task_by_title(args.task)
    if not task:
        print_error(f"Task '{args.task}' not found in project '{project.title}'.")
        return
    task.mark_complete()
    storage.save(users)
    print_success(f"Task '{task.title}' marked as complete ✅")


def cmd_start_task(args, users: dict) -> None:
    """Mark a task as in-progress."""
    user = _get_user(users, args.user)
    project = _get_project(user, args.project)
    task = project.get_task_by_title(args.task)
    if not task:
        print_error(f"Task '{args.task}' not found in project '{project.title}'.")
        return
    task.mark_in_progress()
    storage.save(users)
    print_success(f"Task '{task.title}' marked as in-progress 🔄")


def cmd_summarize_project(args, users: dict) -> None:
    """Use the AI client to summarize a project."""
    user = _get_user(users, args.user)
    project = _get_project(user, args.project)
    print_info("Generating AI summary… (this may take a moment)")
    summary = ai_client.summarize_project(project)
    print_ai_panel(summary, title=f"🤖 Summary: {project.title}")


def cmd_suggest_next(args, users: dict) -> None:
    """Use the AI client to suggest a next step for a project."""
    user = _get_user(users, args.user)
    project = _get_project(user, args.project)
    print_info("Generating next-step suggestion…")
    suggestion = ai_client.suggest_next_step(project)
    print_ai_panel(suggestion, title=f"💡 Next Step: {project.title}")


# ── Argument parser setup ─────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level ArgumentParser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="pm",
        description="📋 Project Management CLI – manage users, projects, and tasks",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # ── add-user ──────────────────────────────────────────────────────────────
    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True, help="User's full name")
    p_add_user.add_argument("--email", required=True, help="User's email address")

    # ── list-users ────────────────────────────────────────────────────────────
    subparsers.add_parser("list-users", help="List all users")

    # ── add-project ───────────────────────────────────────────────────────────
    p_add_proj = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_proj.add_argument("--user", required=True, help="Owner's name")
    p_add_proj.add_argument("--title", required=True, help="Project title")
    p_add_proj.add_argument("--description", default="", help="Project description")
    p_add_proj.add_argument("--due-date", default=None, help="Due date (YYYY-MM-DD)")

    # ── list-projects ─────────────────────────────────────────────────────────
    p_list_proj = subparsers.add_parser("list-projects", help="List projects for a user")
    p_list_proj.add_argument("--user", required=True, help="User's name")

    # ── add-task ──────────────────────────────────────────────────────────────
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--user", required=True, help="Project owner's name")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument("--assigned-to", default="Unassigned", help="Assignee name")

    # ── list-tasks ────────────────────────────────────────────────────────────
    p_list_tasks = subparsers.add_parser("list-tasks", help="List tasks for a project")
    p_list_tasks.add_argument("--user", required=True, help="Project owner's name")
    p_list_tasks.add_argument("--project", required=True, help="Project title")

    # ── complete-task ─────────────────────────────────────────────────────────
    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--user", required=True, help="Project owner's name")
    p_complete.add_argument("--project", required=True, help="Project title")
    p_complete.add_argument("--task", required=True, help="Task title")

    # ── start-task ────────────────────────────────────────────────────────────
    p_start = subparsers.add_parser("start-task", help="Mark a task as in-progress")
    p_start.add_argument("--user", required=True, help="Project owner's name")
    p_start.add_argument("--project", required=True, help="Project title")
    p_start.add_argument("--task", required=True, help="Task title")

    # ── summarize-project ─────────────────────────────────────────────────────
    p_summ = subparsers.add_parser(
        "summarize-project", help="Generate an AI summary of a project"
    )
    p_summ.add_argument("--user", required=True, help="Project owner's name")
    p_summ.add_argument("--project", required=True, help="Project title")

    # ── suggest-next ──────────────────────────────────────────────────────────
    p_suggest = subparsers.add_parser(
        "suggest-next", help="Get an AI next-step suggestion"
    )
    p_suggest.add_argument("--user", required=True, help="Project owner's name")
    p_suggest.add_argument("--project", required=True, help="Project title")

    return parser


# ── Command dispatch ──────────────────────────────────────────────────────────

COMMAND_MAP = {
    "add-user": cmd_add_user,
    "list-users": cmd_list_users,
    "add-project": cmd_add_project,
    "list-projects": cmd_list_projects,
    "add-task": cmd_add_task,
    "list-tasks": cmd_list_tasks,
    "complete-task": cmd_complete_task,
    "start-task": cmd_start_task,
    "summarize-project": cmd_summarize_project,
    "suggest-next": cmd_suggest_next,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Load persisted data
    users = storage.load()

    # Dispatch to the appropriate handler
    handler = COMMAND_MAP.get(args.command)
    if handler:
        handler(args, users)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
