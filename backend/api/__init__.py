import os
import uuid

import requests

from pathlib import Path

from common.configloader import current_config as config
from common.logger import get_logger
from flask import Blueprint, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# TODO: Find a way to refactor this not to import from __main__, cause that's ugly
# (Flask's current_app refuses to work with the rate limiter)
from __main__ import app

logger = get_logger()

api = Blueprint("api", __name__)
limiter = Limiter(get_remote_address, app=app, storage_uri=os.environ["REDIS_URL"])

UPLOADS_DIR = Path(os.environ["UPLOADS"])
GENERATED_DIR = Path(os.environ["GENERATED"])
TEXTGEN_URL = os.environ["TEXTGEN_URL"]


@api.route("/upload", methods=["POST"])
@limiter.limit(config["rate_limits"]["upload"])
def upload():
    if not request.files:
        return jsonify({"error": "no files provided"}), 400

    file_id = uuid.uuid4()

    for i, (name, file) in enumerate(request.files.items()):
        filename = f"{file_id}.{i}"
        file.save(UPLOADS_DIR / filename)

    return jsonify({"id": file_id}), 201


@api.route("/generate", methods=["POST"])
def generate_text():
    response = requests.post(f"http://{TEXTGEN_URL}/generate-text", json=request.json)
    return response.text, response.status_code


@api.route("/status/<task_id>", methods=["GET"])
def check_status(task_id):
    response = requests.get(f"http://{TEXTGEN_URL}/check-status", json={"task_id": task_id})

    json = response.json()
    result = json["result"] if json["state"] not in ("ANALYZING", "GENERATING") else json["state_info"]

    return jsonify(result), response.status_code


@api.route("/text/<text_id>", methods=["GET"])
def get_text(text_id):
    path = GENERATED_DIR / text_id
    if not path.is_file():
        abort(404)
    
    with open(path, "r") as file:
        text = file.read()
    return text
