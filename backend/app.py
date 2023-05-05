import os

from pathlib import Path

from flask import Flask, render_template

frontend_path = Path(os.environ["FRONTEND"])

app = Flask(__name__, static_folder=frontend_path / "static", template_folder=frontend_path / "templates")
app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

host = os.environ["HOST"]
port = int(os.environ["PORT"])


@app.route("/")
def index():
    return render_template("index.pug", static="static")


if __name__ == "__main__":
    app.run(host=host, port=port, debug="DEBUG" in os.environ)