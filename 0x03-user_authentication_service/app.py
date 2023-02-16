#!/usr/bin/env python3
"""
app
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    home route
    """
    return jsonify({"message": "Bievenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
