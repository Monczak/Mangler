import logging
import os
import sys

logger = logging.getLogger("mangler")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s: %(levelname)s/%(module)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

from flask import Flask, jsonify, request
from marshmallow import ValidationError

from schema import TextgenSchema
from tasks import generate_text_task


app = Flask(__name__)
app.config.from_object("flask-config")

host = os.environ["HOST"]
port = int(os.environ["PORT"])


@app.route("/generate_text", methods=["POST"])
def generate_text():
    schema = TextgenSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    task = generate_text_task.delay(data["input_id"], data["train_depths"], data["gen_depth"], data["seed"], data["length"])

    return jsonify({"task_id": task.id}), 202


if __name__ == "__main__":
    app.run(host=host, port=port)