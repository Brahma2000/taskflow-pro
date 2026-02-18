from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.models.user import User
from app.extensions import db

tasks_bp = Blueprint('tasks', __name__)

# CREATE TASK
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    data = request.get_json()

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        user_id=user.id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"}), 201

# GET ALL MY TASKS
@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    tasks = Task.query.filter_by(user_id=user.id).all()
    return jsonify([task.to_dict() for task in tasks])

#GET SINGLE TASK
@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    return jsonify(task.to_dict())

#UPDATE TASK
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    data = request.get_json()

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()

    return jsonify({"message": "Task updated successfully"})

#DELETE TASK
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})
