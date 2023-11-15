#!/usr/bin/env python3
"""
Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET route index

    Returns:
        str: json {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """POST route for user register

    Returns:
        str: messege
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"messege": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login

    Returns:
        str: messege
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ logout

    Return:
       str: message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """profile

    Return:
       str: message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """get_reset_password

    Return:
       str: message
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """update_password

    Return:
       str: message
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_psw = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")


# #!/usr/bin/env python3
# """ Implementing a flask application """

# from auth import Auth
# from typing import Union, Tuple
# from sqlalchemy.orm.exc import NoResultFound
# from flask import Flask, jsonify, request, abort, redirect, url_for

# app = Flask(__name__)
# AUTH = Auth()


# @app.route('/', methods=['GET'], strict_slashes=False)
# def basic_route() -> str:
#     """ Basic route """
#     return jsonify({"message": "Bienvenue"})


# @app.route('/users', methods=['POST'], strict_slashes=False)
# def users() -> Union[str, Tuple]:
#     """ View implementing existence of a user else creating the specified
#         user with email and password provided """
#     try:
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = AUTH.register_user(email, password)
#         return jsonify({"email": email, "message": "user created"})
#     except ValueError:
#         return jsonify({"message": "email already registered"}), 400


# @app.route('/sessions', methods=['POST'], strict_slashes=False)
# def login() -> Union[str, Tuple]:
#     """ View implementing validating user credentials if
#         correct credentials are given a cookie is set on
#         the response else operation is aborted """
#     email = request.form.get('email')
#     password = request.form.get('password')

#     if AUTH.valid_login(email, password):
#         session_id = AUTH.create_session(email)
#         response = jsonify({"email": email, "message": "logged in"})
#         response.set_cookie("session_id", session_id)
#         return response
#     else:
#         abort(401)


# @app.route('/sessions', methods=['DELETE'], strict_slashes=False)
# def logout() -> Union[str, Tuple]:
#     """ View that destroys user's session thus login them out """
#     session_id = request.cookies.get('session_id')
#     user = AUTH.get_user_from_session_id(session_id)

#     if user:
#         AUTH.destroy_session(user.id)
#         return redirect('/')
#     else:
#         abort(403)


# @app.route('/profile', methods=['GET'], strict_slashes=False)
# def profile() -> Tuple:
#     """ View that Informs presence of a user object or not in
#         the database """
#     session_id = request.cookies.get('session_id')
#     user = AUTH.get_user_from_session_id(session_id)

#     if user:
#         return jsonify({"email": user.email}), 200
#     else:
#         abort(403)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port="5000")
