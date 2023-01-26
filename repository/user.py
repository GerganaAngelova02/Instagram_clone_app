from flask import abort

from entity.user import UserEntity
from mapper.user import map_user_entity_to_user_sql_alchemy, \
    map_user_sql_alchemy_to_user_entity
from model import db
from model.user import User
from datetime import datetime


class UserRepository(object):
    def __init__(self, database):
        self.database = database

    def save_user(self, user):
        user_db_model = map_user_entity_to_user_sql_alchemy(user)
        self.database.session.add(user_db_model)
        self.database.session.commit()
        return map_user_sql_alchemy_to_user_entity(user_db_model)

    def get_user_id_by_email(self, email):
        user = self.database.session.query(User).filter(User.email == email).first()
        if user is None:
            abort(404, "User was not found!")
        return user.user_id

    def verify_password(self, user_id, password):
        user = self.database.session.query(User).filter(
            User.user_id == user_id). \
            filter(User.password == password). \
            first()
        if user is None:
            abort(404, "User was not found!")
        return user.username

user_repository = UserRepository(db)