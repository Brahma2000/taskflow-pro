from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
  user_id = get_jwt_identity()

  tasks = Task.query.filter_by(user_id=user_id).all()

  return jsonify([
      {"id": t.id, "title": t.title, "completed": t.completed}
      for t in tasks
  ])

@task_bp.route("/", methods=["POST"])
@jwt_required()
def add_task():
  user_id = get_jwt_identity()
  data = request.get_json()

  task = Task(title=data["title"], user_id=user_id)

  db.session.add(task)
  db.session.commit()

  return jsonify({"message": "Task added"}), 201

@task_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def toggle_task(id):
  task = Task.query.get_or_404(id)

  task.completed = not task.completed
  db.session.commit()

  return jsonify({"message": "Task updated"})

@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
  task = Task.query.get_or_404(id)

  db.session.delete(task)
  db.session.commit()

  return jsonify({"message": "Task deleted"})
