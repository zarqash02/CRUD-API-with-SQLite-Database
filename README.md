# FastAPI Task Management API

A lightweight REST API built with FastAPI and SQLAlchemy for managing a simple task list. The application includes automatic database seeding on startup, creating default tasks if the database is empty.

## Tech Stack & Database Strategy

This project uses **SQLite** as its database engine.

**Why SQLite was chosen:**

* **Zero Configuration:** It requires no separate server process or system-level setup, making it ideal for small projects, prototyping, and rapid development.
* **Portability:** The entire database is contained in a single file, easily shared or deleted to reset the state.
* **Native Support:** Python has built-in support for SQLite, minimizing external dependencies while fully integrating with SQLAlchemy.

**Database Location:**
The database file is generated automatically upon startup and is stored in the root directory of the project as `./tasks.db`.

## How to Start the Project

1. **Install Dependencies**
Ensure you have Python installed, then install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy pydantic

```

2. **Run the Server**
Assuming you saved the code in a file named `main.py`, start the development server using Uvicorn:

```bash
uvicorn main:app --reload

```

3. **Access the API**

* The API will be available at: `[http://127.0.0.1:8000](http://127.0.0.1:8000)`
* View the auto-generated Swagger UI documentation at: `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

## Database Viewer

*(Replace the placeholder below with an actual screenshot of your database viewer, such as DB Browser for SQLite or DBeaver, showing the `tasks` table.)*

## Example SQL Query

If you open the `tasks.db` file in a database viewer, you can execute standard SQL commands to interact with the data independently of the API.

Here is an example query to fetch all tasks that are currently marked as incomplete:

```sql
SELECT id, title, done 
FROM tasks 
WHERE done = 0;

```