"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    def __repr__(self):
        u=self
        return f'<User Id={u.id}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True,
                    nullable=False)
    first_name = db.Column(db.String(30),
                    nullable=False
                    )
    last_name = db.Column(db.String(30),
                    nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """User's Posts"""
    
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f'<Post Id = {p.id}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000))

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)