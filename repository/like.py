from flask import abort, jsonify
from model import db
from model.like import Like
from model.post import Post


class LikeRepository(object):
    def __init__(self, database):
        self.database = database

    def like_unlike_post(self, post_id, user):
        post_to_like_unlike = Post.query.get(post_id)

        if post_to_like_unlike is None:
            abort(404, "Post was not found!")

        check_like = Like.query.filter_by(user_id=user.user_id, post_id=post_id).first()

        # if liked already then we will remove the liked entry (means unlike)
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


like_repository = LikeRepository(db)
