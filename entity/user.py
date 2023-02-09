from schematics.models import Model
from schematics.types import StringType, IntType


class UserEntity(Model):
    email = StringType()
    username = StringType()
    password = StringType()
    full_name = StringType()
    bio = StringType()
    profile_pic = StringType()
    user_id = IntType()
    posts_count = IntType()
    followers_count = IntType()
    following_count = IntType()

    def __repr__(self):
        return vars(self)
