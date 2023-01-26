from entity.user import UserEntity
from form.user_register_form import RegistrationForm
from form.user_login_form import LoginForm
from model.user import User


def map_user_reg_form_to_user_entity(user: RegistrationForm) -> UserEntity:
    return UserEntity({'email': user.email.data,
                       'username': user.username.data,
                       'password': user.password.data,
                       'full_name': user.full_name.data})


def map_user_login_form_to_user_entity(user: LoginForm) -> UserEntity:
    return UserEntity({'email': user.email.data,
                       'password': user.password.data})


def map_user_db_model_to_user_entity(user: User) -> UserEntity:
    return UserEntity({'email': user.email,
                       'username': user.username,
                       'password': user.password,
                       'full_name': user.full_name,
                       'bio': user.bio,
                       'profile_pic': user.profile_pic,
                       'user_id': user.user_id})


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
