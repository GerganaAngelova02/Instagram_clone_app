from model import db


class UserModel(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, index=True)
    user_image_url = db.Column(db.Text)
    password_hash = db.Column(db.String(128))
    # comments = db.relationship('Comment', backref='author_backref', lazy='dynamic')
    # liked = db.relationship('PostLike', backref='user_like_backref', lazy='dynamic')

    def __repr__(self):
        return f"Item {self.username}"
