from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt, bcrypt

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)
  bcrypt.init_app(app)

  from app.routes.auth_routes import auth_bp
  from app.routes.task_routes import tasks_bp

  app.register_blueprint(auth_bp, url_prefix="/auth")
  app.register_blueprint(tasks_bp, url_prefix="/tasks")
  
  return app
