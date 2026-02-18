from app.extensions import db

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  description = db.Column(db.String(500))
  completed = db.Column(db.Boolean, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "completed": self.completed,
      "user_id": self.user_id
    }
