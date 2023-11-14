#!/usr/bin/env python3
""" Implementing a flask application """

from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def basic_route() -> str:
    """ Basic route """
    return jsonify({"message": "Bienvenue"})
