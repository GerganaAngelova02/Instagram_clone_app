from flask import abort

from entity.post import PostEntity
from model import db
from model.post import Post
from mapper.post import map_post_entity_to_post_sql_alchemy, map_post_sql_alchemy_to_post_entity


class PostRepository(object):
    def __init__(self, database):
        self.database = database

    def create_post(self, post):
        post_db_model = map_post_entity_to_post_sql_alchemy(post)
        self.database.session.add(post_db_model)
        self.database.session.commit()
        return map_post_sql_alchemy_to_post_entity(post_db_model)

    def get_all_posts(self):
        result = []
        posts = Post.query.all()
        for post in posts:
            result.append(map_post_sql_alchemy_to_post_entity(post))
        return result

    def get_post(self, post_id):
        post = self.database.session.get(Post, post_id)
        if post is None:
            abort(404, "Post was not found!")
        return post

    def update_post(self, post: PostEntity):
        post_to_check = self.database.session.get(Post, post.post_id)
        if post_to_check is None:
            abort(404, "Post was not found!")
        self.database.session.query(Post). \
            filter(Post.post_id == post.post_id). \
            update({"caption": post.caption})
        self.database.session.commit()

    def delete_post(self, post_id, user_id):
        post = self.database.session.get(Post, post_id)
        if post is None:
            abort(404, "Post was not found!")
        if post.author_id != user_id:
            abort(404, "This post can't be deleted")
        self.database.session.delete(post)
        self.database.session.commit()
        return "Deleted {}".format(map_post_sql_alchemy_to_post_entity(post))


post_repository = PostRepository(db)
