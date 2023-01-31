from schematics.models import Model
from schematics.types import StringType, IntType


class CommentEntity(Model):
    id = IntType()
    comment = StringType()
    user_id = IntType()
    post_id = IntType()

    def __repr__(self):
        return vars(self)