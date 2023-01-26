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

    def __repr__(self):
        return vars(self)
