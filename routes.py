from flask import Blueprint, request, jsonify
from models import TaskManager


task_routes = Blueprint("tasks", __name__)
manager = TaskManager()

VALID_STATUSES = ["pending", "in progress", "completed"]


@task_routes.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Task Manager API!",
        "endpoints": [
            "GET /tasks",
            "GET /tasks/<id>",
            "POST /tasks",
            "PUT /tasks/<id>",
            "PATCH /tasks/<id>/complete",
            "DELETE /tasks/<id>"
        ]
    })


@task_routes.route("/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")

    if status and status not in VALID_STATUSES:
        return jsonify({
            "error": "Invalid status.",
            "valid_statuses": VALID_STATUSES
        }), 400

    tasks = manager.get_all_tasks(status)

    return jsonify({
        "count": len(tasks),
        "tasks": tasks
    }), 200


@task_routes.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = manager.get_task(task_id)

    if task is None:
        return jsonify({
            "error": "Task not found."
        }), 404

    return jsonify(task), 200


@task_routes.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    title = data.get("title")
    description = data.get("description", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Task title is required."
        }), 400

    if not isinstance(description, str):
        return jsonify({
            "error": "Description must be text."
        }), 400

    task = manager.create_task(
        title.strip(),
        description.strip()
    )

    return jsonify({
        "message": "Task created successfully.",
        "task": task
    }), 201


@task_routes.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    existing_task = manager.get_task(task_id)

    if existing_task is None:
        return jsonify({
            "error": "Task not found."
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    title = data.get("title", existing_task["title"])
    description = data.get(
        "description", existing_task["description"]
    )
    status = data.get("status", existing_task["status"])

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Task title must be valid text."
        }), 400

    if not isinstance(description, str):
        return jsonify({
            "error": "Description must be text."
        }), 400

    if not isinstance(status, str) or status not in VALID_STATUSES:
        return jsonify({
            "error": "Invalid status.",
            "valid_statuses": VALID_STATUSES
        }), 400

    task = manager.update_task(
        task_id,
        title.strip(),
        description.strip(),
        status
    )

    return jsonify({
        "message": "Task updated successfully.",
        "task": task
    }), 200


@task_routes.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    existing_task = manager.get_task(task_id)

    if existing_task is None:
        return jsonify({
            "error": "Task not found."
        }), 404

    task = manager.update_task(
        task_id,
        existing_task["title"],
        existing_task["description"],
        "completed"
    )

    return jsonify({
        "message": "Task marked as completed.",
        "task": task
    }), 200


@task_routes.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = manager.delete_task(task_id)

    if not deleted:
        return jsonify({
            "error": "Task not found."
        }), 404

    return jsonify({
        "message": "Task deleted successfully."
    }), 200