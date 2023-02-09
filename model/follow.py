from model import db
from datetime import datetime

#      ____________________________________
#     |   follower_id   |  following_to    |
#     |       1         |       2          |  user with id 1 follows user of id 2
#     |       3         |       1          |  user with id 3 follows user of id 1
#     |       3         |       2          |  user with id 3 also follows user of id 2
#     |_________________|__________________|


class Follow(db.Model):
    __tablename__ = 'follows'

    # id of a person who follows someone (A == follows ==> B)
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    # id of the person to whom we are following to (B == got followed by ==> A)
    following_to = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), primary_key=True)


