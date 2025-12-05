from flask import Flask, Response, jsonify, render_template, request, stream_with_context
from datetime import date as _date, datetime as _datetime
from models.pomodoro import PomodoroTimer
from models.task_manager import TaskManager
from models.task import Task
from models.orm_models import TaskRepository, Base, TaskModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import signal
import sys
if due_str:
    # try parsing ISO date `YYYY-MM-DD`
    try:
        due_date = _date.fromisoformat(due_str)
    except Exception:
        try:
            due_date = _datetime.fromisoformat(due_str).date()
        except Exception:
            due_date = None
app = Flask(__name__)
timer = PomodoroTimer()

# Setup DB and repository (SQLite file `tasks.db` in project root)
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

session = Session()
repo = TaskRepository(session)
task_manager = TaskManager(repository=repo)

def cleanup_on_exit(signum, frame):
    """Clean up resources and exit gracefully"""
    print("\nShutting down server...")
    timer.stop()
    time.sleep(0.2)  # Give threads time to clean up
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, cleanup_on_exit)
signal.signal(signal.SIGTERM, cleanup_on_exit)

@app.route('/')
def home():
    return render_template('index.html', settings=timer)

@app.route("/update_durations", methods=["POST"])
def update_durations():
    data = request.get_json()
    timer.update_durations(
        work=data.get("work"),
        small_break=data.get("small_break"),
        long_break=data.get("long_break")
    )
    return jsonify({"status": "success"})

@app.route("/toggle_timer", methods=["POST"])
def toggle_timer():
    if timer.running:
        timer.stop()
        return jsonify({"status": "stopped"})
    else:
        timer.start()
        return jsonify({"status": "started"})


@app.route("/reset_timer", methods=["POST"])
def reset_timer():
    timer.reset_timer()
    return jsonify(timer.get_state())


@app.route("/reset_durations", methods=["POST"])
def reset_durations():
    timer.reset_durations()
    return jsonify({
        "status": "success",
        "work": timer.work,
        "small_break": timer.small_break,
        "long_break": timer.long_break
    })


@app.route("/prev_state", methods=["POST"])
def prev_state():
    timer.stop()
    timer.prev_state()
    return jsonify(timer.get_state())

@app.route("/next_state", methods=["POST"])
def next_state():
    timer.stop()
    timer.next_state()
    return jsonify(timer.get_state())

@app.route("/get_state", methods=["GET","POST"])
def get_state():
    return jsonify(timer.get_state())


@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    priority = data.get("priority", "Medium")
    due_date = None
    due_str = data.get("due_date")
    if due_str:
        # try parsing ISO date `YYYY-MM-DD`
        try:
            due_date = _date.fromisoformat(due_str)
        except Exception:
            try:
                due_date = _datetime.fromisoformat(due_str).date()
            except Exception:
                due_date = None

    # Create the task and persist; pass a Python date object where possible
    t = task_manager.add_task(title, priority, due_date)
    saved_id = None
    if getattr(task_manager, 'repo', None):
        try:
            # repo.save may have been called inside add_task already; attempt to return id
            saved_id = task_manager.repo.session.query(TaskModel).filter_by(title=title, priority=priority).order_by(TaskModel.id.desc()).first()
            saved_id = saved_id.id if saved_id else None
        except Exception:
            saved_id = None

    return {"status": "ok", "saved_id": saved_id}

@app.route("/tasks")
def list_tasks():
    # Prefer loading directly from repository so tasks reflect database state.
    tasks = None
    if getattr(task_manager, 'repo', None):
        try:
            tasks = task_manager.repo.load_all()
        except Exception:
            tasks = task_manager.show_all_tasks()
    else:
        tasks = task_manager.show_all_tasks()

    out = []
    for T in tasks:
        d = T.to_dict()
        due = d.get('due_date')
        if due and isinstance(due, _date):
            d['due_date'] = due.isoformat()
        out.append(d)

    return {"tasks": out}


@app.route("/db_rows")
def db_rows():
    """Return raw DB rows from the `tasks` table for debugging.

    This endpoint returns the current rows in the DB using SQLAlchemy model.
    """
    try:
        rows = session.query(TaskModel).all()
        out = []
        for r in rows:
            out.append({
                "id": r.id,
                "title": r.title,
                "priority": r.priority,
                "due_date": r.due_date.isoformat() if getattr(r.due_date, 'isoformat', None) else r.due_date,
                "completed": bool(r.completed),
            })
        return {"rows": out}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/sort_priority")
def sort_priority():
    task_manager.sort_priority()
    return {"status": "sorted"}


@app.route("/filter_priority", methods=["GET"])
def filter_priority():
    priority = request.args.get("priority")
    filtered = task_manager.filter_priority(priority)
    return {"tasks": [T.to_dict() for T in filtered]}


@app.route("/reload_tasks", methods=["GET", "POST"])
def reload_tasks():
    """Reload tasks from the repository into the TaskManager in-memory list.

    Supports GET (for quick browser testing) and POST (preferred).
    Returns JSON with status and count. Requires the app to be configured with a repository.
    """
    repo = getattr(task_manager, 'repo', None)
    if not repo:
        return {"status": "no-repository"}, 400
    try:
        task_manager.tasks = repo.load_all() or []
        return {"status": "reloaded", "count": len(task_manager.tasks)}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/sort_due_date")
def sort_due_date():
    task_manager.sort_by_due_date()
    return {"status": "sorted"}


@app.route("/complete_task", methods=["POST"])
def complete_task():
    data = request.json
    title = data.get("title")
    task_manager.mark_complete(title)
    return {"status": "completed"}

@app.route("/delete_task", methods=["POST"])
def delete_task():
    data = request.json
    title = data.get("title")
    task_manager.delete_task(title)
    return {"status": "deleted"}


if __name__ == '__main__':
    try:
        app.run(host="127.0.0.1", port=5001, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        timer.stop()
        exit(0)
    finally:
        # Ensure timer is stopped
        timer.stop()
