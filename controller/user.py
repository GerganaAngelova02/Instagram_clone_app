import flask

from repository.user import UserRepository
from model import db


class UserController(object):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def save_user(self, user):
        return self.user_repository.save_user(user)

    def log_user(self, user):
        return self.user_repository.log_user(user.email, user.password)

    def update_user(self, user):
        self.user_repository.update_user(user)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def get_users_by_username(self, username):
        return self.user_repository.get_user_by_username(username)


user_repository = UserRepository(db)
user_controller = UserController(user_repository)
