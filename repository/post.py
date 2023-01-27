from model import db
from mapper.post import map_post_entity_to_post_sql_alchemy, map_post_sql_alchemy_to_post_entity

class PostRepository(object):
    def __init__(self, database):
        self.database = database

    def create_post(self, post):
        post_db_model = map_post_entity_to_post_sql_alchemy(post)
        self.database.session.add(post_db_model)
        self.database.session.commit()
        return map_post_sql_alchemy_to_post_entity(post_db_model)

post_repository = PostRepository(db)
