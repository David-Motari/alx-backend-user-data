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


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logout endpoint
    """
    session_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(usr.id)
        return redirect('/')
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
