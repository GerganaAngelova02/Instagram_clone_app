from flask import abort
from sqlalchemy import exc

from entity.user import UserEntity
from mapper.user import map_user_entity_to_user_sql_alchemy, \
    map_user_sql_alchemy_to_user_entity
from model import db
from model.user import User
from model.post import Post
from model.comment import Comment
from model.like import Like
from flask_login import LoginManager, login_user


class UserRepository(object):
    def __init__(self, database):
        self.database = database

    def save_user(self, user):
        user_to_check_username = User.query.filter_by(username=user.username).first()
        user_to_check_email = User.query.filter_by(email=user.email).first()
        if user_to_check_username is not None:
            abort(400, "The username is already taken.")
        if user_to_check_email is not None:
            abort(400, "The email is already registered.")
        user_db_model = map_user_entity_to_user_sql_alchemy(user)
        self.database.session.add(user_db_model)
        self.database.session.commit()
        return map_user_sql_alchemy_to_user_entity(user_db_model)

    def log_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return user.username
        else:
            return None

    def update_user(self, user: UserEntity):
        user_to_check = self.database.session.get(User, user.user_id)
        if user_to_check is None:
            abort(404, "User was not found!")
        self.database.session.query(User). \
            filter(User.user_id == user.user_id). \
            update({"username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "password": user.password,
                    "bio": user.bio,
                    "profile_pic": user.profile_pic})
        self.database.session.commit()

    def delete_user(self, user_id):
        user = self.database.session.get(User, user_id)
        if user is None:
            abort(404, "User was not found!")
        self.database.session.query(Post).filter(Post.author_id == user_id).delete()
        self.database.session.query(Comment).filter(Comment.user_id == user_id).delete()
        self.database.session.query(Like).filter(Like.user_id == user_id).delete()
        self.database.session.delete(user)
        self.database.session.commit()
        return "Deleted {}".format(map_user_sql_alchemy_to_user_entity(user))

    def get_user(self, user_id):
        user = self.database.session.get(User, user_id)
        if user is None:
            abort(404, "User was not found!")
        return user

    def get_all_users(self):
        result = []
        users = User.query.all()
        for user in users:
            result.append(map_user_sql_alchemy_to_user_entity(user))
        return result

    def get_user_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(404, "User was not found!")
        return user


user_repository = UserRepository(db)
