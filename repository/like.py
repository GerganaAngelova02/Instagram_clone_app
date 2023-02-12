from flask import abort, jsonify
from model import db
from model.like import Like
from model.post import Post
from model.user import User
from sqlalchemy import func

from repository.user import user_repository


class LikeRepository(object):
    def __init__(self, database):
        self.database = database

    def like_unlike_post(self, post_id, user):
        post_to_like_unlike = Post.query.get(post_id)

        if post_to_like_unlike is None:
            abort(404, "Post was not found!")

        check_like = Like.query.filter_by(user_id=user.user_id, post_id=post_id).first()

        # if liked already then we will remove the record (means unlike)
        if check_like:
            self.database.session.delete(check_like)
            self.database.session.commit()
            return jsonify(
                {"msg": "Post Unliked", "post_id": post_id, "by user": user.username}), 200

        new_like = Like(user_like_backref=user, post_like_backref=post_to_like_unlike)
        self.database.session.add(new_like)
        self.database.session.commit()
        return jsonify(
            {"msg": "Post Liked", "post_id": post_id, "by user": user.username}), 200

    def likes_count(self, post_id):
        query = self.database.session.query(Like.post_id, func.count(Like.id)).group_by(Like.post_id).filter(
            Like.post_id == post_id)
        result = query.all()

        likes_count = [{"post_id": post_id, "likes_count": count} for post_id, count in result if post_id == post_id]
        if len(likes_count) == 0:
            abort(404, "Post was not found!")
            return 0
        else:
            return likes_count[0]

    def likes(self, post_id):
        likes = Like.query.filter_by(post_id=post_id).all()
        user_ids = [like.user_id for like in likes]

        users = [user_repository.get_user(user_id) for user_id in user_ids]
        usernames = [user.username for user in users]
        if usernames is None:
            abort(404, "Post not found or no one liked the post!")
        return usernames


like_repository = LikeRepository(db)
