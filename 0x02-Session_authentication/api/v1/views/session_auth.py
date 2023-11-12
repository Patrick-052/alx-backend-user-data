#!/usr/bin/env python3
""" Module of Session authentication views """

from os import getenv
from typing import Tuple
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request

@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    email = request.form.get("email")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth

        session_id = auth.create_session(getattr(users[0], "id"))
        cookie_name = os.getenv("SESSION_NAME")
        response = jsonify(users[0].to_json())
        response.set_cookie(cookie_name, session_id)

        return response
    else:
        return jsonify({"error": "wrong password"}), 401



# @app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
# def login() -> Tuple[str, int]:
#     """ POST /api/v1/auth_session/login
#     JSON body:
#       - email
#       - password
#     Return:
#       - User object JSON represented
#       - 400 if email or password are missing
#     """
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if email is None or email == '':
#         return jsonify({"error": "email missing"}), 400
#     if password is None or password == '':
#         return jsonify({"error": "password missing"}), 400

#     try:
#         user = User.search({'email': email})
#     except Exception:
#         return jsonify({"error": "no user found for this email"}), 404

#     if not user:
#         return jsonify({"error": "no user found for this email"}), 404

#     user = user[0]
#     if user.is_valid_password(password):
#         from api.v1.app import auth
#         session_id = auth.create_session(user.id)
#         response = jsonify(user.to_json())
#         response.set_cookie(getenv('SESSION_NAME'), session_id)
#         return response
#     else:
#         return jsonify({"error": "wrong password"}), 401
