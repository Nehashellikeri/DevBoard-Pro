from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.project import Project
from app.forms.project_forms import ProjectForm

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('/')
@login_required
def list_projects():
    search = request.args.get('q', '', type=str)
    query = Project.query.filter_by(owner_id=current_user.id)
    if search:
        query = query.filter(Project.name.ilike(f'%{search}%'))
    projects = query.order_by(Project.created_at.desc()).all()
    return render_template('projects/list.html', projects=projects, search=search)


@projects_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data,
            status=form.status.data,
            owner_id=current_user.id,
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html', form=form, title='Add Project')


@projects_bp.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id, owner_id=current_user.id).first_or_404()
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.status = form.status.data
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html', form=form, title='Edit Project')


@projects_bp.route('/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, owner_id=current_user.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('projects.list_projects'))
