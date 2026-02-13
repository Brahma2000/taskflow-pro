from flask import Flask
from config import Config
from app.extensions import db, jwt, migrate

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app, db)

  from app.routes.auth_routes import auth_bp
  from app.routes.task_routes import task_bp

  app.register_blueprint(auth_bp, url_prefix="/auth")
  app.register_blueprint(task_bp, url_prefix="/tasks")
  return app
