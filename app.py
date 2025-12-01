from flask import Flask, Response, jsonify, render_template, request, stream_with_context
from models.pomodoro import PomodoroTimer
from models.task_manager import TaskManager
from models.task import Task
import signal
import sys
import time
app = Flask(__name__) 
timer = PomodoroTimer()
task_manager = TaskManager()

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
    due_date = data.get("due_date")

    task_manager.add_task(title, priority, due_date)
    return {"status": "ok"}

@app.route("/tasks")
def list_tasks():
    return {"tasks": [T.to_dict() for T in task_manager.show_all_tasks()]}

@app.route("/sort_priority")
def sort_priority():
    task_manager.sort_priority()
    return {"status": "sorted"}

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
