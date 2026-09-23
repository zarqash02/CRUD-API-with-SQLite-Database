# Task API

A simple REST API for managing a to-do list, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Database](#database)
- [API Endpoints](#api-endpoints)
- [Inspecting the Database](#inspecting-the-database)
- [Example SQL Query](#example-sql-query)

## Tech Stack

- **FastAPI** — web framework and routing
- **SQLAlchemy** — ORM for talking to the database
- **SQLite** — database engine
- **Pydantic** — request/response validation and schemas
- **Uvicorn** — ASGI server used to run the app

## Prerequisites

- Python 3.9+ installed
- `pip` available on your PATH
- (Optional) [DB Browser for SQLite](https://sqlitebrowser.org/) if you want to inspect the database visually

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/zarqash02/CRUD-API-with-SQLite-Database
cd CRUD-API-with-SQLite-Database
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

If a `requirements.txt` is included in the repo, use that instead:

```bash
pip install -r requirements.txt
```

## Running the Project

Start the API with a single command:

```bash
uvicorn main:app --reload
```

- The API will be available at: `http://127.0.0.1:8000`
- Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

On first run, the app automatically seeds the database with three sample tasks if the `tasks` table is empty.

## Database

This project uses **SQLite** as its database engine.

**Why SQLite?**
- **Single file** — the entire database lives in one `.db` file, with no separate database server to install, configure, or run.
- **Zero setup** — SQLAlchemy connects to it directly via a file path; there's no host, port, username, or password to manage.
- **Survives restarts** — because it's a real file on disk (not in-memory), all tasks persist across app restarts, unlike data that would be lost if the app used an in-memory store.

This makes SQLite ideal for local development and small projects where the overhead of a full database server (like PostgreSQL or MySQL) isn't justified.

**Where the database file lives:**
- The database is stored as `tasks.db` in the project's root directory.
- It is created **automatically** the first time the app starts — you do not need to create it manually.
- `tasks.db` is typically added to `.gitignore`, so it is **not** committed to version control. This means every fresh clone of the repository starts with an empty/newly-seeded database rather than inheriting someone else's data.

## API Endpoints

| Method | Endpoint      | Description                     |
|--------|---------------|----------------------------------|
| GET    | `/`           | API info                        |
| GET    | `/health`     | Health check                    |
| GET    | `/tasks`      | List all tasks                  |
| GET    | `/tasks/{id}` | Get a single task by ID         |
| POST   | `/tasks`      | Create a new task               |
| PUT    | `/tasks/{id}` | Update an existing task         |
| DELETE | `/tasks/{id}` | Delete a task                   |

## Inspecting the Database

You can open `tasks.db` directly in [DB Browser for SQLite](https://sqlitebrowser.org/) to view or query the data:

1. Open DB Browser for SQLite.
2. Choose **Open Database** and select `tasks.db` from the project root.
3. Go to the **Browse Data** tab to view the `tasks` table, or the **Execute SQL** tab to run queries.

**Screenshot:**

image.png

## Example SQL Query


Example

```sql
SELECT id, title, done
FROM tasks
WHERE done = 0;
```

This returns all tasks that are not yet completed.