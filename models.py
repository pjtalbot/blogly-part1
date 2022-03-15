"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

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
    image_url = db.Column(db.String(200), nullable=False, default=DEFAULT_IMAGE_URL)
    # cascade="all, delete-orphan" ensures posts are deleted when user is deleted
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

# association_table = Table('posts_tags', Base.metadata,
#     Column('post_id', ForeignKey('posts.id')),
#     Column('tag_id', ForeignKey('tags.id'))
# )

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

    # tags = db.relationship("Tag", backref='tags')

class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """ Many to Many relationship"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )
