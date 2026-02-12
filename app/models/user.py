from app.extensions import db
from passlib.hash import bcrypt

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)

  def set_password(self, password):
    self.password = bcrypt.hash(password)

  def check_password(self, password):
    return bcrypt.verify(password, self.password)
