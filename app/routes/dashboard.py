from datetime import date
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from app.models.project import Project
from app.models.task import Task

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    tasks = Task.query.filter_by(owner_id=current_user.id).all()

    total_projects = len(projects)
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'Completed'])
    pending_tasks = len([t for t in tasks if t.status != 'Completed'])
    overdue_tasks = len([t for t in tasks if t.is_overdue])

    completion_percent = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    recent_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)[:5]

    status_counts = {
        'To Do': len([t for t in tasks if t.status == 'To Do']),
        'In Progress': len([t for t in tasks if t.status == 'In Progress']),
        'Completed': completed_tasks,
    }
    priority_counts = {
        'High': len([t for t in tasks if t.priority == 'High']),
        'Medium': len([t for t in tasks if t.priority == 'Medium']),
        'Low': len([t for t in tasks if t.priority == 'Low']),
    }

    return render_template(
        'dashboard.html',
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        completion_percent=completion_percent,
        recent_tasks=recent_tasks,
        status_counts=status_counts,
        priority_counts=priority_counts,
    )
