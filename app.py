from datetime import timedelta
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Flask, jsonify, render_template
import os
from flask_cors import CORS
from model import db
# from view.user import index, create_user
from model.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, current_user, JWTManager
from flask_jwt_extended import decode_token, get_jwt
import json
from http import HTTPStatus
# from repository.user import find_user_by_email_and_password
from flask import Response, request, make_response
from controller.user import user_controller
from form.user_register_form import RegistrationForm
from form.user_login_form import LoginForm
from mapper.user import map_user_reg_form_to_user_entity, \
    map_user_db_model_to_user_entity, map_user_login_form_to_user_entity

from flask_login import LoginManager



def create_app():
    app = Flask(__name__)
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
        # return render_template("index.html")
        return "DIDO"

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

    # @app.route('/login', methods=['POST'])
    # def login():
    #     login_form = LoginForm(request.form)
    #     if not login_form.validate():
    #         return Response(json.dumps(login_form.errors),
    #                         status=HTTPStatus.BAD_REQUEST,
    #                         mimetype='application/json')
    #     user_entity = map_user_login_form_to_user_entity(login_form)
    #     response = user_controller.log_user(user_entity)
    #     return Response(json.dumps(response), status=HTTPStatus.OK)

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
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.password == login_form.password.data:
            login_user(user)
            response = {'status': 'success', 'user': user.username}
        else:
            response = {'status': 'fail', 'message': 'Invalid email or password'}
        return Response(json.dumps(response), status=HTTPStatus.OK)


    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
