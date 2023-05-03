from logger import setup_logger

setup_logger()

import os

from flask import Flask, jsonify, request
from marshmallow import ValidationError

from schema import TextgenSchema, CheckStatusSchema
from tasks import generate_text_task, get_result


app = Flask(__name__)
app.config.from_object("flask_config")

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


@app.route("/check_status", methods=["GET"])
def check_status():
    schema = CheckStatusSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    task_result = get_result(data["task_id"])
    state = task_result.state
    state_info = task_result.info if state in ("ANALYZING", "GENERATING") else None

    # Catch any exception the task potentially raised, because get() reraises exceptions
    try:
        result = task_result.get() if state in ("SUCCESS", "FAILURE") else None
        real_state = "FAILURE" if result and result["result"] != "success" else state
    except Exception as err:
        result = None
        real_state = "INTERNAL_ERROR"

    return jsonify({"state": real_state, 
                    "state_info": state_info, 
                    "result": None if not result else {key: value for key, value in result.items() if key != "result"}}
                    ), 200


if __name__ == "__main__":
    app.run(host=host, port=port)