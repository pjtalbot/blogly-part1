from pickle import NONE
from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name='Mike', last_name="Talbot", image_url="https://images.unsplash.com/photo-1628890920690-9e29d0019b9b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80")
u2 = User(first_name='Matt', last_name="Talbot", image_url='https://images.unsplash.com/photo-1564156280315-1d42b4651629?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=784&q=80')

p1 = Post(title='Sup!', content="I am Paul's big bro!", user_id=2)

db.session.add(u1)
db.session.add(u2)
db.session.commit()

db.session.add(p1)
db.session.commit()