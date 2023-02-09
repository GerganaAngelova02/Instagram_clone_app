from flask import abort, jsonify
from model import db
from model.follow import Follow
from model.user import User

from entity.user import UserEntity


class FollowRepository(object):
    def __init__(self, database):
        self.database = database

    def is_following(self, cur_user, user):
        if user.user_id is None:
            return False

        return cur_user.following_to_list.filter_by(following_to=user.user_id).first() is not None

    def follow_user(self, cur_user, username):
        user = User.query.filter_by(username=username).first()

        if user is None:
            abort(404, "User not found!")
        elif user.username == cur_user.username:
            abort(403, "You cannot follow yourself.")
        else:
            if self.is_following(cur_user, user):
                abort(403, "Already following the user.")
            else:
                follow_data = Follow(follower_backref=cur_user,
                                     following_to_backref=user)
                db.session.add(follow_data)
                db.session.commit()
                return {"msg": f"Started following {username}."}

    def unfollow_user(self, cur_user, username):
        user = User.query.filter_by(username=username).first()

        if user is None:
            abort(404, "User not found!")
        else:
            if not self.is_following(cur_user, user):
                abort(403, "Not following this user.")
            else:
                user_to_unfollow = cur_user.following_to_list.filter_by(
                    following_to=user.user_id).first()
                if user_to_unfollow:
                    db.session.delete(user_to_unfollow)
                db.session.commit()
                return {"msg": f"Unfollowed {username}."}

    def get_followers_list(self, username):
        user = User.query.filter_by(username=username).first()

        if user is None:
            abort(404, "User not found")

        followers_data = []
        if user.username == username:
            followers = user.followers_list.all()
            for each_follower in followers:
                locate_user = User.query.get(each_follower.follower_id)
                followers_data.append(locate_user.username)
            return {"followers": followers_data}
        else:
            abort(405, "not allowed.")

    def number_of_followers(self, username):
        return len(self.get_followers_list(username))

    def get_following_list(self, username):
        user = User.query.filter_by(username=username).first()

        if user is None:
            abort(404, "User not found")

        following_data = []
        if user.username == username:
            following = user.following_to_list.all()
            for each in following:
                locate_user = User.query.get(each.following_to)
                following_data.append(locate_user.username)
            return {"following list": following_data}
        else:
            abort(405, "not allowed.")

    def number_of_following(self, username):
        return len(self.get_following_list(username))


follow_repository = FollowRepository(db)
