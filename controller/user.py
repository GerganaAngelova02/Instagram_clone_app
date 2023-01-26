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
        user_id = self.user_repository.get_user_id_by_email(user.email)
        username = self.user_repository.verify_password(user_id, user.password)
        return username


user_repository = UserRepository(db)
user_controller = UserController(user_repository)
