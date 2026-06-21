# 📋 Project Management CLI Tool

A Python-based Command-Line Interface for managing users, projects, and tasks — with an integrated AI assistant powered by the Project Summary Service API.

---

## 📁 File Structure

```
project-management-cli/
├── main.py                  # CLI entry point (argparse + command dispatch)
├── models/
│   ├── __init__.py
│   ├── user.py              # Person base class + User subclass
│   ├── project.py           # Project class with task management
│   └── task.py              # Task class with status transitions
├── services/
│   ├── __init__.py
│   ├── storage_service.py   # JSON file I/O for persistence
│   └── ai_client.py         # Project Summary Service API client (summaries & suggestions)
├── utils/
│   ├── __init__.py
│   └── formatters.py        # rich-powered CLI output helpers
├── data/
│   └── project_data.json    # Auto-generated local data store
├── requirements.txt
└── README.md
```

---

## ✨ Features

- **User management** — add and list users
- **Project management** — create projects per user with descriptions and due dates
- **Task management** — add tasks, assign them, mark as in-progress or complete
- **Data persistence** — all data saved locally in `data/project_data.json` via JSON
- **Rich CLI output** — colour-coded tables and panels via the `rich` package
- **AI summaries** — generate project summaries and next-step suggestions via the Project Summary Service API

---

## 🛠 Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/project-management-cli.git
cd project-management-cli
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the AI client (optional)

Set your Project Summary Service API key as an environment variable:

```bash
export ="sk-ant-..."   # macOS/Linux
set =sk-ant-...        # Windows CMD
```

If the key is not set, all other commands work normally and AI features will display a friendly message.

---

## 🚀 How to Run

```bash
python main.py <command> [options]
```

Run `python main.py --help` to see all available commands.

---

## 📖 Example Commands

```bash
# Add users
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py add-user --name "Jordan" --email "jordan@example.com"

# List all users
python main.py list-users

# Add projects to a user
python main.py add-project --user "Alex" --title "CLI Tool" \
  --description "Build project tracker" --due-date "2025-08-01"

# List projects for a user
python main.py list-projects --user "Alex"

# Add tasks to a project
python main.py add-task --user "Alex" --project "CLI Tool" \
  --title "Implement add-task command" --assigned-to "Alex"
python main.py add-task --user "Alex" --project "CLI Tool" \
  --title "Write README" --assigned-to "Jordan"

# List tasks
python main.py list-tasks --user "Alex" --project "CLI Tool"

# Update task status
python main.py start-task --user "Alex" --project "CLI Tool" \
  --task "Implement add-task command"
python main.py complete-task --user "Alex" --project "CLI Tool" \
  --task "Implement add-task command"

# AI features (requires )
python main.py summarize-project --user "Alex" --project "CLI Tool"
python main.py suggest-next --user "Alex" --project "CLI Tool"
```

---

## 🤖 AI Client Feature

The `services/ai_client.py` module wraps the Project Summary Service API using the `project summary service` PyPI package. It exposes two methods used by the CLI:

| Command | Description |
|---|---|
| `summarize-project` | 2-sentence summary + risk note + next step |
| `suggest-next` | Single actionable next-step recommendation |

The service layer is intentionally separated from the CLI so that `main.py` only handles argument parsing and output, while `AIClient` handles all external API interaction. Failures are caught gracefully so the CLI never crashes on AI errors.

---

## ⚙️ OOP Design Highlights

| Feature | Where |
|---|---|
| Inheritance (`Person → User`) | `models/user.py` |
| `@property` / setters with validation | `user.py`, `project.py`, `task.py` |
| Class-level ID counters | All three model classes |
| `__str__` / `__repr__` | All three model classes |
| One-to-many relationships | `User → Projects`, `Project → Tasks` |
| JSON serialization (`to_dict` / `from_dict`) | All three model classes |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `rich` | Formatted tables, panels, and coloured CLI output |
| `project summary service` | Project Summary Service API client for AI summaries and suggestions |

---

## ⚠️ Known Issues / Limitations

- User names are used as unique keys (case-insensitive). Two users with the same name are not supported.
- No authentication or role-based access control.
- AI features require an active internet connection and a valid ``.
- Data is stored in a single flat JSON file; not suited for large datasets.

---

## 📜 License

MIT
