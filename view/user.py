import json
from http import HTTPStatus

from flask import Response, request, make_response
from controller.user import user_controller
from form.user_register_form import RegistrationForm
from mapper.user import map_user_reg_form_to_user_entity, \
    map_user_db_model_to_user_entity


# def index():
#     return "DIDO"
#
#
# def create_user():
#     reg_form = RegistrationForm(request.form)
#     if not reg_form.validate():
#         return Response(json.dumps(reg_form.errors),
#                         status=HTTPStatus.BAD_REQUEST,
#                         mimetype='application/json')
#     user = map_user_reg_form_to_user_entity(reg_form)
#     response = user_controller.save_user(user)
#     return Response(json.dumps(response), status=HTTPStatus.OK)
