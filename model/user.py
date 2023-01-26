from model import db


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
