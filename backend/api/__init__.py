import os
import uuid

import requests

from pathlib import Path

from common.configloader import current_config as config
from common.logger import get_logger
from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# TODO: Find a way to refactor this not to import from __main__, cause that's ugly
# (Flask's current_app refuses to work with the rate limiter)
from __main__ import app

logger = get_logger()

api = Blueprint("api", __name__)
limiter = Limiter(get_remote_address, app=app, storage_uri=os.environ["REDIS_URL"])

UPLOAD_DIR = Path(os.environ["UPLOADS"])


@api.route("/upload", methods=["POST"])
@limiter.limit(config["rate_limits"]["upload"])
def upload():
    file_id = uuid.uuid4()

    if not request.files:
        return jsonify({"error": "no files provided"}), 400

    for i, (name, file) in enumerate(request.files.items()):
        filename = f"{file_id}.{i}"
        file.save(UPLOAD_DIR / filename)

    return jsonify({"id": file_id}), 201
