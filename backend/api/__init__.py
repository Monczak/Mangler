import os
import uuid

import requests

from pathlib import Path

from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from __main__ import app

api = Blueprint("api", __name__)
limiter = Limiter(get_remote_address, app=app, storage_uri=os.environ["REDIS_URL"])

UPLOAD_DIR = Path(os.environ["UPLOADS"])


@api.route("/upload", methods=["POST"])
@limiter.limit("10/minute") # TODO: Load this from a config file
def upload():
    file_id = uuid.uuid4()

    for i, (name, file) in enumerate(request.files.items()):
        filename = f"{file_id}.{i}"
        file.save(UPLOAD_DIR / filename)

    return jsonify({"id": file_id}), 202
