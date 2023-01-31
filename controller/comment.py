import flask

from repository.comment import CommentRepository
from model import db


class CommentController(object):
    def __init__(self, comment_repository):
        self.comment_repository = comment_repository

    def create_comment(self, comment):
        return self.comment_repository.create_comment(comment)

    def get_comments(self, post_id):
        return self.comment_repository.get_comments(post_id)


comment_repository = CommentRepository(db)
comment_controller = CommentController(comment_repository)
