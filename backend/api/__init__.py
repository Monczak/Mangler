import os
import shutil
import uuid

import requests

from pathlib import Path

from common.configloader import current_config as config
from common.logger import get_logger
from exampleloader import current_examples as examples
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
EXAMPLES_DIR = os.environ["EXAMPLES"]


@api.route("/upload", methods=["POST"])
@limiter.limit(config["rate_limits"]["upload"])
def upload():
    # if not request.files:
    #     return jsonify({"error": "no files provided"}), 400

    file_id = uuid.uuid4()

    for i, (name, file) in enumerate(request.files.items()):
        filename = f"{file_id}.{i}"
        file.save(UPLOADS_DIR / filename)

    return jsonify({"id": file_id, "ttl": config["cleanup"]["uploads_min_lifetime"]}), 201


@api.route("/generate", methods=["POST"])
def generate_text():
    # Not using Marshmallow for validation here as we only need to handle examples if they're present
    # Also, validating other parts of the request is the textgen's job and it'll handle unknown keys too
    if "examples" in request.json.keys():
        if not isinstance(request.json["examples"], list) or any(not isinstance(example, str) for example in request.json["examples"]):
            return jsonify({"examples": ["Invalid data."]}), 400

        if "input_id" in request.json.keys():
            for i, example in enumerate(request.json["examples"]):
                if (EXAMPLES_DIR / f"{example}.txt").is_file():
                    shutil.copy(EXAMPLES_DIR / f"{example}.txt", UPLOADS_DIR / f"{request.json['input_id']}.example{i}")

    response = requests.post(f"http://{TEXTGEN_URL}/generate-text", json={key: value for key, value in request.json.items() if key != "examples"})
    return response.text, response.status_code


@api.route("/status/<task_id>", methods=["GET"])
def check_status(task_id):
    response = requests.get(f"http://{TEXTGEN_URL}/check-status", json={"task_id": task_id})
    if response.status_code == 404:
        abort(404)

    json = response.json()
    result = json["result"] if json["state"] not in ("ANALYZING", "GENERATING") else json["state_info"]
    result["state"] = json["state"]

    return jsonify(result), response.status_code


@api.route("/text/<text_id>", methods=["GET"])
def get_text(text_id):
    path = GENERATED_DIR / text_id
    if not path.is_file():
        abort(404)
    
    with open(path, "r") as file:
        text = file.read()
    return text, 200


@api.route("/examples", methods=["GET"])
def get_examples():
    return jsonify(examples), 200 if examples else 204
