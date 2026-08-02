from datetime import datetime, date
from app.extensions import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='To Do')       # To Do / In Progress / Completed
    priority = db.Column(db.String(10), default='Medium')     # High / Medium / Low
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'Completed':
            return self.due_date < date.today()
        return False

    def __repr__(self):
        return f'<Task {self.title}>'
