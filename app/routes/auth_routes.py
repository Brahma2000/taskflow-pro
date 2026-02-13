from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["post"])
def register():
  data = request.get_json()

  user = User(username=data["username"])
  user.set_password(data["password"])

  db.session.add(user)
  db.session.commit()

  return jsonify({"message": "User registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
  data = request.get_json()

  user = User.query.filter_by(username=data["username"]).first()

  if not user or not user.check_password(data["password"]):
    return jsonify({"error": "Invalid credentials"}), 401

  token = create_access_token(identify=user.id)

  return jsonify(access_token=token)
