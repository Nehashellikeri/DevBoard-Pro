import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, login_manager

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # ---- Config ----
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///devboard.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    os.makedirs(app.instance_path, exist_ok=True)

    # ---- Init extensions ----
    db.init_app(app)
    login_manager.init_app(app)

    # ---- Import models so SQLAlchemy knows about them ----
    from app.models.user import User
    from app.models.project import Project
    from app.models.task import Task

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---- Register blueprints ----
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.projects import projects_bp
    from app.routes.tasks import tasks_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(profile_bp)

    # ---- Create tables on first run ----
    with app.app_context():
        db.create_all()

    return app
