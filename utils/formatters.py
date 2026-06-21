"""
utils/formatters.py
CLI output helpers using the `rich` library for formatted tables and panels.
Falls back to plain print() if rich is not installed.
"""

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


def print_success(message: str) -> None:
    """Print a success message in green."""
    if RICH_AVAILABLE:
        console.print(f"[bold green]✔ {message}[/bold green]")
    else:
        print(f"✔ {message}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    if RICH_AVAILABLE:
        console.print(f"[bold red]✘ {message}[/bold red]")
    else:
        print(f"✘ ERROR: {message}")


def print_info(message: str) -> None:
    """Print an info/neutral message."""
    if RICH_AVAILABLE:
        console.print(f"[cyan]{message}[/cyan]")
    else:
        print(message)


def print_users_table(users: dict) -> None:
    """Display all users in a formatted table."""
    if not users:
        print_info("No users found.")
        return

    if RICH_AVAILABLE:
        table = Table(title="👥 All Users", box=box.ROUNDED, show_lines=True)
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", style="bold cyan")
        table.add_column("Email", style="magenta")
        table.add_column("Projects", justify="right", style="green")

        for user in users.values():
            table.add_row(
                str(user.user_id),
                user.name,
                user.email,
                str(len(user.projects)),
            )
        console.print(table)
    else:
        print("\n=== All Users ===")
        for user in users.values():
            print(f"  [{user.user_id}] {user.name} <{user.email}> | Projects: {len(user.projects)}")


def print_projects_table(user) -> None:
    """Display all projects for a user in a formatted table."""
    if not user.projects:
        print_info(f"No projects found for user '{user.name}'.")
        return

    if RICH_AVAILABLE:
        table = Table(
            title=f"📁 Projects for {user.name}",
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title", style="bold cyan")
        table.add_column("Description")
        table.add_column("Due Date", style="yellow")
        table.add_column("Tasks", justify="center")
        table.add_column("Done %", justify="right", style="green")

        for p in user.projects:
            stats = p.completion_summary()
            table.add_row(
                str(p.project_id),
                p.title,
                p.description or "—",
                p.due_date,
                f"{stats['complete']}/{stats['total']}",
                f"{stats['percent_done']}%",
            )
        console.print(table)
    else:
        print(f"\n=== Projects for {user.name} ===")
        for p in user.projects:
            print(str(p))


def print_tasks_table(project) -> None:
    """Display all tasks for a project in a formatted table."""
    if not project.tasks:
        print_info(f"No tasks found for project '{project.title}'.")
        return

    if RICH_AVAILABLE:
        status_colors = {
            "complete": "green",
            "in-progress": "yellow",
            "pending": "dim",
        }
        table = Table(
            title=f"📋 Tasks for '{project.title}'",
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title", style="bold")
        table.add_column("Assigned To", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Created At", style="dim")

        for t in project.tasks:
            color = status_colors.get(t.status, "white")
            table.add_row(
                str(t.task_id),
                t.title,
                t.assigned_to,
                f"[{color}]{t.status}[/{color}]",
                t.created_at,
            )
        console.print(table)
    else:
        print(f"\n=== Tasks for '{project.title}' ===")
        for t in project.tasks:
            print(str(t))


def print_ai_panel(content: str, title: str = "🤖 AI Summary") -> None:
    """Display AI-generated content in a styled panel."""
    if RICH_AVAILABLE:
        console.print(Panel(content, title=title, border_style="bright_blue"))
    else:
        print(f"\n--- {title} ---")
        print(content)
        print("-" * 40)
