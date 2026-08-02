import csv
import io
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user

from app.extensions import db
from app.models.task import Task
from app.models.project import Project
from app.forms.task_forms import TaskForm

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


def _project_choices():
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    return [(p.id, p.name) for p in projects]


@tasks_bp.route('/')
@login_required
def list_tasks():
    search = request.args.get('q', '', type=str)
    query = Task.query.filter_by(owner_id=current_user.id)
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))
    tasks = query.order_by(Task.created_at.desc()).all()
    return render_template('tasks/list.html', tasks=tasks, search=search)


@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    form.project_id.choices = _project_choices()

    if not form.project_id.choices:
        flash('Create a project first before adding tasks.', 'warning')
        return redirect(url_for('projects.add_project'))

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            project_id=form.project_id.data,
            owner_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))

    return render_template('tasks/form.html', form=form, title='Add Task')


@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    form.project_id.choices = _project_choices()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.project_id = form.project_id.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))

    return render_template('tasks/form.html', form=form, title='Edit Task')


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, owner_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/export/csv')
@login_required
def export_csv():
    tasks = Task.query.filter_by(owner_id=current_user.id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Project', 'Status', 'Priority', 'Due Date', 'Created At'])
    for t in tasks:
        writer.writerow([
            t.title,
            t.project.name if t.project else '',
            t.status,
            t.priority,
            t.due_date.strftime('%Y-%m-%d') if t.due_date else '',
            t.created_at.strftime('%Y-%m-%d'),
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=devboard_tasks.csv'
    return response
