# 📋 Project Management CLI Tool

A Python-based Command-Line Interface (CLI) application for managing users, projects, and tasks. The application demonstrates object-oriented programming concepts, JSON-based data persistence, modular design, and command-line interaction using Python.

---

## Repository

GitHub Repository: https://github.com/trivekram-s/project-management-cli-python

**Author:** Trivekram

---

## 📁 Project Structure

```text
project-management-cli-python/
├── main.py                  # CLI entry point
├── models/
│   ├── __init__.py
│   ├── user.py              # User model
│   ├── project.py           # Project model
│   └── task.py              # Task model
├── services/
│   ├── __init__.py
│   └── storage_service.py   # JSON file persistence
├── utils/
│   ├── __init__.py
│   └── formatters.py        # CLI output formatting
├── data/
│   └── project_data.json    # Local data storage
├── requirements.txt
└── README.md
```

---

## ✨ Features

* Add and manage users
* Create projects for users
* Add tasks to projects
* Update task status
* View users, projects, and tasks
* Store data locally using JSON
* Rich formatted terminal output
* Object-Oriented Programming design
* Modular project structure

---

## 🛠 Prerequisites

* Python 3.10 or later
* Git

Verify installation:

```bash
python --version
git --version
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/trivekram-s/project-management-cli-python.git
cd project-management-cli-python
```

### 2. Create a Virtual Environment (Optional but Recommended)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Display available commands:

```bash
python main.py --help
```

General syntax:

```bash
python main.py <command> [options]
```

---

## 📖 Example Usage

### Add a User

```bash
python main.py add-user --name "Alex" --email "alex@example.com"
```

### List Users

```bash
python main.py list-users
```

### Add a Project

```bash
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build project tracker"
```

### List Projects

```bash
python main.py list-projects --user "Alex"
```

### Add a Task

```bash
python main.py add-task --user "Alex" --project "CLI Tool" --title "Implement add-task command"
```

### List Tasks

```bash
python main.py list-tasks --user "Alex" --project "CLI Tool"
```

### Start a Task

```bash
python main.py start-task --user "Alex" --project "CLI Tool" --task "Implement add-task command"
```

### Complete a Task

```bash
python main.py complete-task --user "Alex" --project "CLI Tool" --task "Implement add-task command"
```

---

## 🏗 Object-Oriented Design

### Classes

#### User

* Name
* Email
* Projects

#### Project

* Title
* Description
* Due Date
* Tasks

#### Task

* Title
* Status
* Assigned User

### Relationships

* One User → Many Projects
* One Project → Many Tasks

### OOP Concepts Demonstrated

* Classes and Objects
* Inheritance
* Properties and Setters
* Class Attributes
* Object Relationships
* JSON Serialization
* Modular Design

---

## 💾 Data Persistence

All application data is stored locally in:

```text
data/project_data.json
```

The file is automatically created and updated as users, projects, and tasks are added or modified.

---

## 📦 Dependencies

| Package | Purpose                                              |
| ------- | ---------------------------------------------------- |
| rich    | Enhanced CLI tables, formatting, and terminal output |

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## ⚠️ Limitations

* Data is stored in a single JSON file.
* No authentication system.
* User names must be unique.
* Designed for learning and demonstration purposes.

---

## 🧪 Testing

Verify available commands:

```bash
python main.py --help
```

Check project data:

```bash
python main.py list-users
python main.py list-projects --user "Alex"
```

---

## 📜 License

This project was created for learning and training purposes.
