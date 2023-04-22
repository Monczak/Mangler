import os

from flask import Flask, jsonify, request

from tasks import generate_text_task

app = Flask(__name__)
app.config.from_object("flask-config")

host = os.environ["HOST"]
port = int(os.environ["PORT"])


@app.route("/generate_text", methods=["POST"])
def generate_text():
    input_id = request.json["input_id"]
    
    task = generate_text_task.delay(input_id)

    return jsonify({"task_id": task.id}), 202


if __name__ == "__main__":
    app.run(host=host, port=port)