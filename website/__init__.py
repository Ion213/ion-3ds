from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

#create database object
db=SQLAlchemy()
DB_NAME ="database.db"

#create migration so that you can migrate youre models(using cmd)
migrate = Migrate()

#create flask app
def flask_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'ion21'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(app.root_path, DB_NAME))
    #inheret the database and mirgration to the main app(flask app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    #implement login manager(sessions)
    login_manager = LoginManager()
    login_manager.login_view = '/'
    login_manager.init_app(app)
    from .sessions.session_storage import User
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
        
    # Import routes/blueprints
    from .controller.admin_auth import admin_auth
    app.register_blueprint(admin_auth, url_prefix='/')
    from .routes.admin_views import admin_views
    app.register_blueprint(admin_views, url_prefix='/')
    from .routes.public_views import public_views
    app.register_blueprint(public_views, url_prefix='/')

    
    #craeate database
    create_database(app)
    
    return app

# Create database function
def create_database(app):
    if not os.path.exists(os.path.join(app.root_path, DB_NAME)):
        with app.app_context():
            db.create_all()
