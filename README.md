# Task Management REST API

A RESTful API built with Flask and SQLite for managing tasks. Includes full CRUD operations, input validation, status filtering, and PyTest unit tests.

## Tech Stack
- **Python** — core language
- **Flask** — web framework
- **SQLite + SQLAlchemy** — database and ORM
- **PyTest** — unit testing

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/abhiram2607/task-management-api
cd task-management-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Get all tasks (optional `?status=` filter) |
| GET | `/tasks/<id>` | Get a task by ID |
| PUT | `/tasks/<id>` | Update a task |
| DELETE | `/tasks/<id>` | Delete a task |

## Example Request

```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix bug #42", "description": "Null pointer in auth module", "status": "in_progress"}'

# Get all done tasks
curl http://localhost:5000/tasks?status=done
```

## Task Status Values
- `pending` (default)
- `in_progress`
- `done`

## Running Tests

```bash
pytest test_app.py -v
```

Expected output: **17 tests passing**

## Project Structure

```
task-management-api/
├── app.py              # Flask app and API routes
├── test_app.py         # PyTest unit tests (17 tests)
├── requirements.txt    # Dependencies
└── README.md
```
