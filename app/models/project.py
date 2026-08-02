from datetime import datetime
from app.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Active')  # Active / Completed / On Hold
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    @property
    def total_tasks(self):
        return len(self.tasks)

    @property
    def completed_tasks(self):
        return len([t for t in self.tasks if t.status == 'Completed'])

    @property
    def progress_percent(self):
        if not self.tasks:
            return 0
        return round((self.completed_tasks / self.total_tasks) * 100)

    def __repr__(self):
        return f'<Project {self.name}>'
