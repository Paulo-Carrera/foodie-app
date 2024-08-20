from datetime import datetime 
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

def connect_db(app):
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()
db = SQLAlchemy()



class User(db.Model):

        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), nullable=False, unique=True)
        password = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(50), nullable=False, unique=True)
        first_name = db.Column(db.String(30), nullable=False)
        last_name = db.Column(db.String(30), nullable=False)
        image_url = db.Column(db.String(200), nullable=False, default="/static/images/default-pic.png")
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
