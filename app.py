import flask
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Flask, jsonify, render_template, url_for
import os
from flask_cors import CORS
from os.path import join, dirname, realpath
from mapper.post import map_post_db_model_to_post_entity
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from form.comment import CommentForm
from model import db
from model.user import User
import json
from http import HTTPStatus
# from repository.user import find_user_by_email_and_password
from flask import Response, request, make_response
from controller.user import user_controller
from controller.post import post_controller
from controller.like import like_controller
from form.user_register_form import RegistrationForm
from form.user_login_form import LoginForm
from form.user_settings_form import SettingsForm
from form.post_form import PostForm
from entity.post import PostEntity
from mapper.user import map_user_reg_form_to_user_entity, \
    map_user_db_model_to_user_entity, map_user_login_form_to_user_entity, map_user_settings_form_to_user_entity
from mapper.comment import map_comment_post_form_to_comment_entity, map_comment_db_model_to_comment_entity
from flask_login import LoginManager, current_user
from controller.comment import comment_controller


def create_app():
    app = Flask(__name__, static_folder="static")
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER', 'admin'),
        os.getenv('DB_PASSWORD', 'password'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_PORT', '3307'),
        os.getenv('DB_NAME', 'db')
    )

    db.init_app(app)

    #
    # app.add_url_rule('/', view_func=index)
    # app.add_url_rule('/register', methods=['POST'], view_func=create_user())
    #
    # return app

    @app.route('/')
    def index():
        return "GerriGram"

    @app.route('/register', methods=['POST'])
    def create_user():
        reg_form = RegistrationForm(request.form)
        if not reg_form.validate():
            return Response(json.dumps(reg_form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')
        user = map_user_reg_form_to_user_entity(reg_form)
        response = user_controller.save_user(user)
        return Response(json.dumps(response), status=HTTPStatus.OK)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['POST'])
    def login():
        login_form = LoginForm(request.form)
        if not login_form.validate():
            return Response(json.dumps(login_form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')
        user = map_user_login_form_to_user_entity(login_form)
        username = user_controller.log_user(user)
        if username:
            response = {'status': 'success', 'user': username}
        else:
            response = {'status': 'fail', 'message': 'Invalid email or password'}
        return Response(json.dumps(response), status=HTTPStatus.OK)

    @app.route('/settings', methods=['POST'])
    @login_required
    def settings():
        settings_form = SettingsForm(request.form)
        if not settings_form.validate():
            return Response(json.dumps(settings_form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')
        user = map_user_settings_form_to_user_entity(settings_form)
        user.user_id = current_user.user_id
        user_controller.update_user(user)
        # return {"id": user.user_id, "bio": user.bio, "pic": user.profile_pic}
        return Response(status=HTTPStatus.OK)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return Response(json.dumps("You have logged out"), status=HTTPStatus.OK)

    @app.route('/user', methods=['GET'])
    @login_required
    def get_user():
        user = user_controller.get_user(current_user.user_id)
        user_entity = map_user_db_model_to_user_entity(user)
        return flask.jsonify({"username": user_entity.username,
                              "email": user_entity.email,
                              "full_name": user_entity.full_name,
                              "bio": user_entity.bio,
                              "profile_pic": user_entity.profile_pic})

    @app.route('/users', methods=['GET'])
    def get_all_users():
        return flask.jsonify(user_controller.get_all_users())

    @app.route('/user/delete', methods=['DELETE'])
    @login_required
    def delete_user():
        return user_controller.delete_user(current_user.user_id)

    app.config["UPLOAD_FOLDER"] = join(dirname(realpath(__file__)), "static/uploads")

    app.config["MAX_CONTENT_LENGTH"] = 1000 * 1024 * 1024  # 1000mb

    app.config['WTF_CSRF_ENABLED'] = False
    csrf = CSRFProtect(app)

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def create_post():
        form = PostForm(request.form)
        if not form.validate():
            return Response(json.dumps(form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')

        allowed_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.bmp'}

        content = request.files['content']
        file_ext = os.path.splitext(content.filename)[1].lower()
        if file_ext not in allowed_extensions:
            error_message = "Invalid file type. Only photo files are allowed."
            return Response(json.dumps(error_message), status=HTTPStatus.BAD_REQUEST)

        content.save(secure_filename(content.filename))
        file_url = request.host_url + content.filename
        post_entity = PostEntity({'caption': form.caption.data,
                                  'content': file_url,
                                  'author_id': current_user.user_id})
        response = post_controller.create_post(post_entity)
        return Response(json.dumps(response), status=HTTPStatus.OK)

    @app.route('/posts', methods=['GET'])
    def get_all_posts():
        return flask.jsonify(post_controller.get_all_posts())

    @app.route('/post/<post_id>', methods=['GET'])
    @login_required
    def get_post(post_id):
        post = post_controller.get_post(post_id)
        post_entity = map_post_db_model_to_post_entity(post)
        return flask.jsonify({"post_id": post_entity.post_id,
                              "caption": post_entity.caption,
                              "content": post_entity.content,
                              "author_id": post_entity.author_id})

    @app.route('/post/<post_id>', methods=['POST'])
    @login_required
    def update_post(post_id):
        form = PostForm(request.form)
        if not form.validate():
            return Response(json.dumps(form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')
        post = PostEntity({'caption': form.caption.data})
        post.post_id = post_id
        post_controller.update_post(post)
        return Response(status=HTTPStatus.OK)

    @app.route('/post/<post_id>', methods=['DELETE'])
    @login_required
    def delete_post(post_id):
        user_id = current_user.user_id
        return post_controller.delete_post(post_id, user_id)

    @app.route('/post/<post_id>/like_unlike', methods=['POST', 'DELETE'])
    @login_required
    def like_unlike_post(post_id):
        return like_controller.like_unlike_post(post_id, current_user)

    @app.route('/post/<post_id>/likes_count', methods=['GET'])
    @login_required
    def likes_count(post_id):
        return flask.jsonify(like_controller.likes_count(post_id))

    @app.route('/post/<post_id>/likes', methods=['GET'])
    @login_required
    def likes(post_id):
        return flask.jsonify(like_controller.likes(post_id))

    @app.route('/post/<post_id>/comment', methods=['POST'])
    @login_required
    def create_comment(post_id):
        form = CommentForm(request.form)
        if not form.validate():
            return Response(json.dumps(form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')

        comment = map_comment_post_form_to_comment_entity(form)
        comment.user_id = current_user.user_id
        comment.post_id = post_id
        response = comment_controller.create_comment(comment)
        return Response(json.dumps(response), status=HTTPStatus.OK)

    @app.route('/post/<post_id>/comments', methods=['GET'])
    @login_required
    def get_comments(post_id):
        return flask.jsonify(comment_controller.get_comments(post_id))

    @app.route('/post/<post_id>/comment/<com_id>', methods=['GET'])
    @login_required
    def get_comment(post_id, com_id):
        comment_to_get = comment_controller.get_comment(post_id, com_id)
        comment = map_comment_db_model_to_comment_entity(comment_to_get)
        return flask.jsonify(comment.to_primitive())

    @app.route('/post/<post_id>/comment/<com_id>', methods=['DELETE'])
    @login_required
    def delete_comment(post_id, com_id):
        comment_controller.delete_comment(post_id, com_id, current_user.user_id)
        return Response(status=HTTPStatus.OK)

    @app.route('/post/<post_id>/comment/<com_id>', methods=['POST'])
    @login_required
    def update_comment(post_id, com_id):
        form = CommentForm(request.form)
        if not form.validate():
            return Response(json.dumps(form.errors),
                            status=HTTPStatus.BAD_REQUEST,
                            mimetype='application/json')
        comment = map_comment_post_form_to_comment_entity(form)
        comment.id = com_id
        comment.post_id = post_id
        comment_controller.update_comment(comment, current_user.user_id)
        return Response(status=HTTPStatus.OK)

    app.config['UPLOAD_FOLDER']
    app.config['UPLOADED_FILES_DEST'] = '/path/to/uploaded/files'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
