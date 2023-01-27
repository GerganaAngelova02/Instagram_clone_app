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

    # comments = db.relationship('Comment', backref='author_backref', lazy='dynamic')
    # liked = db.relationship('PostLike', backref='user_like_backref', lazy='dynamic')

    # sending follower in the first column of table
    # keeps the record/list of users which current user is following to
    # example if user1 follows user2 and user3 we have => [<Follow 1, 2>, <Follow 1, 3>]
    # following_to_list = db.relationship(
    #     'Follow',
    #     foreign_keys=[Follow.follower_id],
    #     backref=db.backref('follower_backref', lazy='joined'),
    #     lazy='dynamic',
    #     cascade='all, delete-orphan'  # description at end
    # )
    #
    # # sending following_to in the second column of table
    # # keeps the record/list of users which follows our current user
    # # example if user3 follows user1 (current user) we have => [<Follow 3, 1>]
    # got_followed_back_list = db.relationship(
    #     'Follow',
    #     foreign_keys=[Follow.following_to],
    #     backref=db.backref('following_to_backref', lazy='joined'),
    #     lazy='dynamic',
    #     cascade='all, delete-orphan'  # description at end
    # )

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
