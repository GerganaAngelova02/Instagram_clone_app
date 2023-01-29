from model import db
from repository.like import LikeRepository


class LikeController(object):
    def __init__(self, like_repository):
        self.like_repository = like_repository

    def like_unlike_post(self, post_id, user):
        return self.like_repository.like_unlike_post(post_id, user)


like_repository = LikeRepository(db)
like_controller = LikeController(like_repository)
