"""Blogly application."""
from crypt import methods
import datetime
import sqlalchemy
from flask import Flask, request, redirect, render_template
from sqlalchemy import text, select
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap



# To Do:
# Input validation
    # Trailing Spaces
    # no numbers
    # validate url
# basic layout
# NavBar (accessible)
# Make pytests
# add datetime to User Model
# make "sort functionality" for users and posts



# change "anchor" tags. anchor tags are often inaccessible. it's not a "semantic element"

# find visual techniques for navigating code.






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

all_tags = Tag.query.all()

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
    """ adds New User to Database """

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url =request.form['image_url'] or None

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
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')

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


@app.route('/users/<int:user_id>/post', methods=["GET", "POST"])
def add_post(user_id):
    """Posts the post :) """

    user = User.query.get_or_404(user_id)

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user)

    db.session.add(new_post)
    db.session.commit()

    tags = (request.form['tags']).lower().split()
    print(tags)

    all_tag_objs = Tag.query.all()

    all_tag_names = []
    for tag_objs in all_tag_objs:
        all_tag_names.append(tag_objs.name)

    


    for tag in tags:
        # check here if tag already exists
        # if it does, retreive tag and make new PostTag with existing ID
        if tag in all_tag_names:
            this_tag_id = Tag.query.filter_by(name=tag).first().id
            post_tag_id = PostTag(
                post_id = new_post.id,
                tag_id = this_tag_id
            )
            db.session.add(post_tag_id)
            db.session.commit()

        else:
            new_tag = Tag(
                name=tag
            )
            db.session.add(new_tag)
            db.session.commit()

            tag_id = PostTag(
                post_id = new_post.id,
                tag_id = new_tag.id
            )
        db.session.add(tag_id)
        

    db.session.commit()

    

    return redirect(f"/users/{user_id}")

@app.route('/users/<int:user_id>/<int:post_id>', methods=["GET"])
def view_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    tags = post.tags

    tags_list = []

    
    # tag_names = tags.name
    
    

    # names = db.session.select([text('name')]).select_from(tags.join(posts_tags, tags.c.id == posts_tags.c.tag_id))

    # for pId, tId in tag_ids:
    #     name = Tag.query.filter(Tag.id == tId)
    #     filtered_names.append(name)


    
    
    # def get_tag_ids():
    #     tags = Tag    
    # tag_names = db.session.query(Post, Tag).join(Tag).all()

    

    # for post, tag in tags:
    #     filtered_names.append(tag.name)


  
    # tags = PostTag.query.get_or_404(tag_id).filter_by(post_id = post.id)
    
    # use post_id to gather list of tags.

    return render_template('view_post.html', user=user, post=post, tags=tags)

@app.route('/users/<int:user_id>/<int:post_id>/edit', methods=['POST'])
def show_edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    tags_list = []
    for tag in tags:
        tags_list.append(tag.name)
    tags_str = ' '.join(tags_list)

    
    return render_template('edit_post.html', user=user, post=post, tags=tags)

@app.route('/users/<int:user_id>/<int:post_id>', methods=["POST"])
def update_post(user_id, post_id):
    """ posts user edits to database """

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = post.tags


    post.title = request.form['title']
    post.content = request.form['content']
    #  remove all tags?
    
    updated_tag_ids = request.form.getlist('tag_checkbox')
    
    print('_______--------_______')
    print(tags)
    print('_______--------_______')

    for tag in tags:
        if str(tag.id) not in updated_tag_ids:
            # remove PostTag
            PostTag.query.filter_by(post_id=post_id, tag_id=tag.id).delete()

    all_tag_objs = Tag.query.all()

    all_tag_names = []
    for tag_objs in all_tag_objs:
        all_tag_names.append(tag_objs.name)

    new_tags = (request.form['tags']).lower().split()
    
    for tag in new_tags:
        # check here if tag already exists
        # if it does, retreive tag and make new PostTag with existing ID
        if tag in all_tag_names:
            this_tag_id = Tag.query.filter_by(name=tag).first().id
            post_tag_id = PostTag(
                post_id = post.id,
                tag_id = this_tag_id
            )
            db.session.add(post_tag_id)
            db.session.commit()

        else:
            new_tag = Tag(
                name=tag
            )
            db.session.add(new_tag)
            db.session.commit()

            tag_id = PostTag(
                post_id = post.id,
                tag_id = new_tag.id
            )
            db.session.add(tag_id)


    # make set of current tags with id's

    
    
    post.tags
    # for tag in tags:
    #     # check here if tag already exists
    #     # if it does, retreive tag and make new PostTag with existing ID
    #     existing_tags = tags.query.all()
    #     existing_tag_names = []
        
    #     new_tag = Tag(
    #         name=tag
    #     )
    #     db.session.add(new_tag)
    #     db.session.commit()

    #     tag_id = PostTag(
    #         post_id = new_post.id,
    #         tag_id = new_tag.id
    #     )
    #     db.session.add(tag_id)

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

# how to organize tags
    # should be added when creating posts

    # -------- Tags ---------

@app.route('/tags', methods=["GET"])
def show_tags_page():
    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)

@app.route('/tags/<int:tag_id>', methods=["GET"])
def show_posts_with_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag_posts.html', posts=posts, tag=tag)

# @app.route(/)

