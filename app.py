"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/', methods=["GET"])
def root():
    """List users and show add form"""


    return redirect("/users")

@app.route('/users', methods=["GET"])
def list_users():
    """List users and show add form"""

    users = User.query.all()

    return render_template("base.html", users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Show "create new user" form """

    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Show "create new user" form """

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show selected user's profile"""

    user = User.query.get_or_404(user_id)
    return render_template('show_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_user(user_id):
    """Show selected user's profile"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """ posts user edits to database """

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """"Deletes User"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


