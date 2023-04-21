from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.from_object("config")


@app.route("/generate_text", methods=["POST"])
def generate_text():
    input_files = request.json["input_files"]
    

    return jsonify({"task_id": 0}), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)