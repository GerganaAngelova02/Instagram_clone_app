from schematics.models import Model
from schematics.types import StringType, IntType


class PostEntity(Model):
    post_id = IntType()
    caption = StringType()
    content = StringType()
    author_id = IntType()

    def __repr__(self):
        return vars(self)
