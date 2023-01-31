from entity.comment import CommentEntity
from model.comment import Comment
from form.comment import CommentForm


def map_comment_post_form_to_comment_entity(comment: CommentForm) -> CommentEntity:
    return CommentEntity({'comment': comment.comment.data})


def map_comment_entity_to_comment_sql_alchemy(comment: CommentEntity) -> Comment:
    return Comment(id=comment.id,
                   comment=comment.comment,
                   user_id=comment.user_id,
                   post_id=comment.post_id)


def map_comment_sql_alchemy_to_comment(comment: Comment) -> dict:
    return dict(CommentEntity({'id': comment.id,
                               'comment': comment.comment,
                               'user_id': comment.user_id,
                               'post_id': comment.post_id}))
