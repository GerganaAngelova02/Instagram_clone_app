import flask

from repository.user import UserRepository
from model import db


class UserController(object):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def save_user(self, user):
        users = self.user_repository.save_user(user)
        return users

    def log_user(self, user):
        username = self.user_repository.log_user(user.email, user.password)
        return username

    def update_user(self, user):
        self.user_repository.update_user(user)


user_repository = UserRepository(db)
user_controller = UserController(user_repository)
