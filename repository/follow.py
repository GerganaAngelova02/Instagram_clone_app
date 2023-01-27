from flask import abort
from model import db
from model.follow import Follow
from entity.user import UserEntity



class FollowRepository(object):
    def __init__(self, database):
        self.database = database


