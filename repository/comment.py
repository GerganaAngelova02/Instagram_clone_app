from flask import abort

from entity.comment import CommentEntity
from model import db
from model.comment import Comment
from model.user import User
from mapper.comment import map_comment_entity_to_comment_sql_alchemy, map_comment_sql_alchemy_to_comment
from repository.user import user_repository

class CommentRepository(object):
    def __init__(self, database):
        self.database = database

    def create_comment(self, comment):
        comment_db_model = map_comment_entity_to_comment_sql_alchemy(comment)
        self.database.session.add(comment_db_model)
        self.database.session.commit()
        return map_comment_sql_alchemy_to_comment(comment_db_model)

    def get_comments(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        if comments:
            comments_with_username = []
            for comment in comments:
                user = User.query.get(comment.user_id)
                comments_with_username.append({"comment": comment.comment, "username": user.username})
            return comments_with_username
        else:
            return None

comment_repository = CommentRepository(db)
