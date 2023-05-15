from common.logger import setup_logger
setup_logger()

import os

import states

from flask import Flask, jsonify, request
from marshmallow import ValidationError

from schema import TextgenRequestSchema, CheckStatusSchema
from tasks import generate_text_task, get_result


app = Flask(__name__)
app.config.from_object("flask_config")

host = os.environ["HOST"]
port = int(os.environ["PORT"])


@app.route("/generate-text", methods=["POST"])
def generate_text():
    schema = TextgenRequestSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    task = generate_text_task.delay(data["input_id"], data["train_depths"], data["gen_depth"], data["seed"], data["length"], data["temperature"])

    return jsonify({"task_id": task.id}), 202


@app.route("/check-status", methods=["GET"])
def check_status():
    schema = CheckStatusSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    task_result = get_result(data["task_id"])
    state = task_result.state
    state_info = task_result.info if state in (states.ANALYZING, states.GENERATING) else None

    # Catch any exception the task potentially raised, because get() reraises exceptions
    try:
        result = task_result.get() if state in (states.SUCCESS, states.FAILURE) else None
        real_state = states.FAILURE if result and result["result"] != "success" else state
    except Exception as err:
        result = None
        real_state = states.INTERNAL_ERROR

    return jsonify({"state": real_state, 
                    "state_info": state_info, 
                    "result": None if not result else {key: value for key, value in result.items() if key != "result"}}
                    ), \
                        200 if real_state in (states.SUCCESS) else \
                        202 if real_state in (states.ANALYZING, states.GENERATING) else \
                        400 if real_state in (states.FAILURE) else \
                        404 if real_state in (states.PENDING) else \
                        500


if __name__ == "__main__":
    app.run(host=host, port=port)