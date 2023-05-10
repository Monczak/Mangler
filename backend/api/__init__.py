import requests

from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)


@api.route("/upload", methods=["POST"])
def upload():
    response = str(request.files)
    return jsonify(response), 202