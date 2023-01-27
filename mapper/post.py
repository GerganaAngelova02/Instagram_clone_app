from entity.post import PostEntity
from model.post import Post


def map_post_entity_to_post_sql_alchemy(post: PostEntity) -> Post:
    return Post(post_id=post.post_id,
                caption=post.caption,
                content=post.content,
                author_id=post.author_id)


def map_post_sql_alchemy_to_post_entity(post: Post) -> dict:
    return dict(PostEntity({'post_id': post.post_id,
                            'caption': post.caption,
                            'content': post.content,
                            'author_id': post.author_id}))
