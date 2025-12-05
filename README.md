# Prioriti

CS122 Semester Project  
**Authors:** Anishka Chauhan, Bineet Anand

A Pomodoro timer and task management web application built with Flask, Tailwind CSS, and SQLite.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Building Tailwind CSS](#building-tailwind-css)
- [Database Management](#database-management)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.11+** (check with `python3 --version`)
- **Node.js & npm** (check with `node --version` and `npm --version`)
- **Conda** (optional, for virtual environment management)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Prioriti
```

### 2. Create a Virtual Environment (Recommended)

Using conda:
```bash
conda create -n prioriti-env python=3.11
conda activate prioriti-env
```

Or using venv:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install flask sqlalchemy
```

### 4. Install Node.js Dependencies

```bash
npm install
```

This installs Tailwind CSS, PostCSS, and Autoprefixer as development dependencies.

---

## Running the Application

### 1. Build Tailwind CSS

Before starting the server, compile the Tailwind CSS:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
```

**Or** use the npm script for watch mode (auto-rebuilds on file changes):

```bash
npm run watch:css
```

This command will continuously monitor your CSS files and rebuild automatically whenever you make changes.

### 2. Start the Flask Server

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5001`

---

## Building Tailwind CSS

### One-Time Build (Minified)

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
```

### Watch Mode (Development)

For automatic CSS rebuilds while developing:

```bash
npm run watch:css
```

This opens a file watcher that rebuilds `static/dist/output.css` whenever you modify files in:
- `templates/` (HTML files)
- `static/src/` (CSS files)

---

## Database Management

### Creating the Database

The database (`tasks.db`) is created automatically when the Flask app starts. SQLite tables are initialized from the ORM models.

### Inspecting the Database

View all stored tasks:

```bash
sqlite3 tasks.db "SELECT id, title, priority, due_date, completed FROM tasks;"
```

### Reloading Tasks from Database

If the database was modified externally, reload tasks into the app:

```bash
curl -X POST http://127.0.0.1:5001/reload_tasks
```

Or open in your browser:

```
http://127.0.0.1:5001/reload_tasks
```

---

## API Endpoints

### Timer Endpoints

- `GET /get_state` – Get current timer state (minutes, seconds, state label)
- `POST /toggle_timer` – Start/pause the timer
- `POST /reset_timer` – Reset the timer to the current state's duration
- `POST /next_state` – Move to the next Pomodoro state (Work → Break → Long Break → Work)
- `POST /prev_state` – Move to the previous state
- `POST /update_durations` – Update work/break durations (JSON: `{work, small_break, long_break}`)
- `POST /reset_durations` – Reset to default durations

### Task Endpoints

- `POST /add_task` – Add a new task (JSON: `{title, priority, due_date}`)
- `GET /tasks` – Fetch all tasks
- `POST /complete_task` – Mark a task as completed (JSON: `{title}`)
- `POST /delete_task` – Delete a task (JSON: `{title}`)
- `GET /filter_priority?priority=High` – Filter tasks by priority
- `POST /sort_priority` – Sort tasks by priority (High → Medium → Low)
- `POST /sort_due_date` – Sort tasks by due date (earliest first)

### Debugging Endpoints

- `GET /db_rows` – View raw database rows (for diagnostics)
- `POST /reload_tasks` – Reload tasks from database into memory

---

## Directory Structure

```
Prioriti/
├── app.py                       # Flask application entry point
├── models/
│   ├── task.py                 # Task model
│   ├── task_manager.py         # Task management logic
│   ├── orm_models.py           # SQLAlchemy ORM models & repository
│   └── pomodoro.py             # Pomodoro timer logic
├── templates/
│   ├── index.html              # Main UI (timer, tasks, settings)
│   └── timer.html              # Timer page (if used separately)
├── static/
│   ├── src/
│   │   └── input.css           # Tailwind CSS source
│   └── dist/
│       └── output.css          # Compiled CSS (generated)
├── tasks.db                     # SQLite database (auto-created)
├── package.json                # Node.js dependencies
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── README.md                   # This file
```

---

## Troubleshooting

### "Module not found" Errors

Ensure all dependencies are installed:

```bash
pip install flask sqlalchemy
npm install
```

### Tailwind CSS Not Loading

1. Rebuild CSS:
   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
   ```

2. Verify the link in `templates/index.html`:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='dist/output.css') }}">
   ```

3. Clear browser cache and refresh.

### Tasks Not Persisting

1. Check that `tasks.db` exists in the project root.
2. Verify the `/add_task` response includes a `saved_id`:
   ```bash
   curl -X POST http://127.0.0.1:5001/add_task \
     -H "Content-Type: application/json" \
     -d '{"title":"Test","priority":"High","due_date":"2025-12-05"}'
   ```

3. Inspect the database:
   ```bash
   curl http://127.0.0.1:5001/db_rows
   ```

### SQLite Date Type Error

Ensure the server parses `due_date` strings into Python date objects. This should happen automatically in `/add_task`. If you see a date error, restart the server:

```bash
python app.py
```

### Session Rolled Back Errors

If the database session fails (e.g., invalid data), the session is rolled back automatically. Restart the server to clear the error state:

```bash
# Stop the server (Ctrl+C) and restart
python app.py
```

---

## Development Tips

1. **Watch Mode for CSS**: Run `npm run watch:css` in a separate terminal while developing to avoid manual rebuilds.

2. **Debug Database**: Use `/db_rows` endpoint to inspect current database state without using SQLite CLI.

3. **Reload Tasks**: Call `/reload_tasks` if you modify the database directly outside the app.

4. **Browser DevTools**: Open DevTools (F12) to inspect network requests and see what data is being sent/received.

---

## License

CS122 Course Project
