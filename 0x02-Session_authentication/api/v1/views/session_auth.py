#!/usr/bin/env python3
""" Module of Session authentication views """

from os import getenv
from models.user import User
from typing import Tuple, Dict
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login() -> Tuple[str, int]:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if email or password are missing
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)
        return response
    else:
        return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    JSON body:
      - session_id
    Return:
      - Empty JSON if session_id is None
      - 404 if session_id doesn't exist
      - 200 and destroy session_id if it exists
    """
    from api.v1.app import auth
    logout = auth.destroy_session(request)
    if logout is False:
        abort(404)
    else:
        return jsonify({}), 200
