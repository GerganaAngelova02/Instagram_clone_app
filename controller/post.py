import flask

from repository.post import PostRepository
from model import db


class PostController(object):
    def __init__(self, post_repository):
        self.post_repository = post_repository

    def create_post(self, post):
        return self.post_repository.create_post(post)

    # def log_user(self, user):
    #     return self.user_repository.log_user(user.email, user.password)
    #
    # def update_user(self, user):
    #     self.user_repository.update_user(user)
    #
    # def delete_user(self, user_id):
    #     return self.user_repository.delete_user(user_id)
    #
    # def get_user(self,user_id):
    #     return self.user_repository.get_user(user_id)
    #
    # def get_all_users(self):
    #     return self.user_repository.get_all_users()


post_repository = PostRepository(db)
post_controller = PostController(post_repository)
