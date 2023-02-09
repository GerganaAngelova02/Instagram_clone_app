from model import db
from repository.follow import FollowRepository


class FollowController(object):
    def __init__(self, follow_repository):
        self.follow_repository = follow_repository

    def follow_user(self, cur_user, username):
        return follow_repository.follow_user(cur_user, username)

    def unfollow_user(self, cur_user, username):
        return follow_repository.unfollow_user(cur_user, username)

    def get_followers_list(self,username):
        return follow_repository.get_followers_list(username)

    def get_following_list(self,username):
        return follow_repository.get_following_list(username)


follow_repository = FollowRepository(db)
follow_controller = FollowController(follow_repository)
