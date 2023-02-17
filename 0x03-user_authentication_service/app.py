#!/usr/bin/env python3
"""
app
"""
from flask import Flask, jsonify
from auth import Auth
from flask import request, abort, redirect


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    register user
    """
    try:
        email = request.form["email"]
        password = request.form["password"]
    except Exception:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    implements log and creates session_id
    """
    email = request.form["email"]
    password = request.form["password"]
    if AUTH.valid_login(email, password) is False:
        abort(401)
    else:
        session_id = AUTH.create_session(email=email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logout endpoint that destroys the session id
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    gets user profile based on session_id
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    endpoint for resetting user password
    """
    try:
        email = request.form["email"]
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    endpoint for updating password
    """
    try:
        email = request.form["email"]
        reset_token = request.form["reset_token"]
        new_password = request.form["new_password"]
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
