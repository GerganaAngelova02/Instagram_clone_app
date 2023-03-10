from entity.user import UserEntity
from form.user_register_form import RegistrationForm
from form.user_login_form import LoginForm
from form.user_settings_form import SettingsForm
from model.user import User
from repository.follow import follow_repository
from repository.post import post_repository


def map_user_reg_form_to_user_entity(user: RegistrationForm) -> UserEntity:
    return UserEntity({'email': user.email.data,
                       'username': user.username.data,
                       'password': user.password.data,
                       'full_name': user.full_name.data})


def map_user_login_form_to_user_entity(user: LoginForm) -> UserEntity:
    return UserEntity({'email': user.email.data,
                       'password': user.password.data})


def map_user_settings_form_to_user_entity(user: SettingsForm, file_path) -> UserEntity:
    return UserEntity({'email': user.email.data,
                       'username': user.username.data,
                       'password': user.password.data,
                       'full_name': user.full_name.data,
                       'bio': user.bio.data,
                       'profile_pic': file_path})


def map_user_db_model_to_user_entity(user: User) -> UserEntity:
    return UserEntity({'email': user.email,
                       'username': user.username,
                       'password': user.password,
                       'full_name': user.full_name,
                       'bio': user.bio,
                       'profile_pic': user.profile_pic,
                       'user_id': user.user_id,
                       'followers_count': follow_repository.number_of_followers(user.username),
                       'following_count': follow_repository.number_of_following(user.username),
                       'posts_count': post_repository.number_of_posts(user.user_id)})


def map_user_entity_to_user_sql_alchemy(user: UserEntity) -> User:
    return User(user_id=user.user_id,
                email=user.email,
                username=user.username,
                password=user.password,
                full_name=user.full_name,
                bio=user.bio,
                profile_pic=user.profile_pic)


def map_user_sql_alchemy_to_user_entity(user: User) -> dict:
    return dict(UserEntity({'email': user.email,
                            'username': user.username,
                            'password': user.password,
                            'full_name': user.full_name,
                            'bio': user.bio,
                            'profile_pic': user.profile_pic,
                            'user_id': user.user_id}))
