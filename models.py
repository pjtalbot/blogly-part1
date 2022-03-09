"""Models for Blogly."""
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
        return f'<User Id=(u.id)>'

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

