#!/usr/bin/env python3
"""
session_auth for views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /auth_session/login
    handles all routes for the Session authentication
    """
    user_email = request.form.get("email")
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_password = request.form.get("password")
    if not user_password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(user_password):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            u_json = jsonify(user.to_json())
            u_json.set_cookie(getenv("SESSION_NAME"), session_id)
            return u_json
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    endpoit for logging-out
    """
    from api.v1.app import auth

    des_session = auth.destroy_session(request)
    if des_session is False:
        abort(404)
    else:
        return jsonify({}), 200
