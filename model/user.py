from model import db
from model.follow import Follow


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_pic = db.Column(db.Text)
    liked = db.relationship('Like', backref='user_like_backref', lazy='dynamic')
    comments = db.relationship('Comment', backref='user_comment_backref', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete')

    following_to_list = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower_backref', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    followers_list = db.relationship(
        'Follow',
        foreign_keys=[Follow.following_to],
        backref=db.backref('following_to_backref', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"User {self.username}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id
