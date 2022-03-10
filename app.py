"""Blogly application."""
from crypt import methods
import datetime
from flask import Flask, request, redirect, render_template
from sqlalchemy import TIMESTAMP
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

# To Do:
# Input validation
# basic layout
# NavBar (accessible)



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

@app.route('/users/<int:user_id>/post', methods=["GET"])
def show_post_form(user_id):
    """Shows Post Form"""

    user = User.query.get_or_404(user_id)

    return render_template('new_post_form.html', user=user)


@app.route('/users/<int:user_id>/post', methods=["POST"])
def add_post(user_id):
    """Posts the post :) """

    user = User.query.get_or_404(user_id)

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/users/<int:user_id>/<int:post_id>', methods=["GET"])
def view_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    return render_template('view_post.html', user=user, post=post)

@app.route('/users/<int:user_id>/<int:post_id>/edit', methods=['POST'])
def show_edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    return render_template('edit_post.html', user=user, post=post)

@app.route('/users/<int:user_id>/<int:post_id>', methods=["POST"])
def update_post(user_id, post_id):
    """ posts user edits to database """

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)


    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    
    return redirect(f'/users/{user.id}/{post.id}')

@app.route('/users/<int:user_id>/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id, user_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

    # Finish "delete_post"
