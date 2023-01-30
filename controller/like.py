from model import db
from repository.like import LikeRepository


class LikeController(object):
    def __init__(self, like_repository):
        self.like_repository = like_repository

    def like_unlike_post(self, post_id, user):
        return self.like_repository.like_unlike_post(post_id, user)

    def likes_count(self, post_id):
        return self.like_repository.likes_count(post_id)

    def likes(self, post_id):
        return self.like_repository.likes(post_id)


like_repository = LikeRepository(db)
like_controller = LikeController(like_repository)
