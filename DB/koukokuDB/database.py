"""FlaskアプリがSQLAlchemyを使えるようにするための初期化"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    Migrate(app, db)

def reset_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
