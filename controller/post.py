import flask

from repository.post import PostRepository
from model import db


class PostController(object):
    def __init__(self, post_repository):
        self.post_repository = post_repository

    def create_post(self, post):
        return self.post_repository.create_post(post)

    def get_all_posts(self):
        return self.post_repository.get_all_posts()

    def user_posts(self,user_id):
        return self.post_repository.user_posts(user_id)

    def get_post(self, post_id):
        return self.post_repository.get_post(post_id)

    def update_post(self, post):
        self.post_repository.update_post(post)

    def delete_post(self, post_id, user_id):
        return self.post_repository.delete_post(post_id, user_id)


post_repository = PostRepository(db)
post_controller = PostController(post_repository)
