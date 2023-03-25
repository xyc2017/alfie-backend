from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='abcdefg'
    app.config['SQLALCHEMY_DATABASE_URI']=('postgresql://xyc2017:v2_42Q9S_NyjeWSec4QdkuZ7WnBRR3Sa@db.bit.io:5432/xyc2017/capstone')
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
def create_database(app):
    if not path.exists('alfieBackend'+ 'postgresql://xyc2017:v2_42Q9S_NyjeWSec4QdkuZ7WnBRR3Sa@db.bit.io:5432/xyc2017/capstone'):
        db.create_all(app=app)
        print('created dated')