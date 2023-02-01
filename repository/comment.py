from flask import abort

from entity.comment import CommentEntity
from model import db
from model.comment import Comment
from model.post import Post
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

    def get_comment(self, post_id, com_id):
        post = self.database.session.get(Post, post_id)
        if post is None:
            abort(404, "Post was not found!")
        comment = self.database.session.query(Comment).join(Post). \
            filter(Post.post_id == post_id). \
            filter(Comment.id == com_id). \
            first()
        if comment is None:
            abort(404, "Comment was not found!")
        return comment

    def delete_comment(self, post_id, com_id, cur_user_id):
        comment_to_delete = self.get_comment(post_id, com_id)
        post = self.database.session.get(Post, post_id)
        if comment_to_delete is None:
            abort(404, "Comment was not found!")
        if comment_to_delete.user_id == cur_user_id:
            self.database.session.delete(comment_to_delete)
            self.database.session.commit()
        elif cur_user_id == post.author_id:
            self.database.session.delete(comment_to_delete)
            self.database.session.commit()
        else:
            abort(404, "You can not delete this comment!")

    def update_comment(self, comment: CommentEntity, cur_user_id):
        comment_to_update = self.get_comment(comment.post_id, comment.id)
        if comment_to_update is None:
            abort(404, "Comment was not found!")
        if comment_to_update.user_id == cur_user_id:
            self.database.session.query(Comment). \
                filter(Comment.post_id == comment.post_id). \
                filter(Comment.id == comment.id). \
                update({"comment": comment.comment})
            self.database.session.commit()
        else:
            abort(404, "You can not update this comment!")



comment_repository = CommentRepository(db)
