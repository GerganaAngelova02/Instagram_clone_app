from model import db
from model.comment import Comment
from model.like import Like

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    likes = db.relationship('Like', backref='post_like_backref', lazy='dynamic',cascade='all, delete')
    comments = db.relationship('Comment', backref='post_comment_backref', lazy='dynamic', cascade='all, delete')

    def __repr__(self):
        return '<Comment %r>' % self.post_id
