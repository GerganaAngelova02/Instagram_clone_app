from model import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(200), index=True)
    body = db.Column(db.Text)
    # body_html = db.Column(db.Text)
    uploaded_content_url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
