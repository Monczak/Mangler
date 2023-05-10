import os

import api

from pathlib import Path

from flask import Flask, render_template


frontend_path = Path(os.environ["FRONTEND"])

app = Flask(__name__, static_folder=frontend_path / "static", template_folder=frontend_path / "templates")
app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

app.register_blueprint(api.api, url_prefix="/api")

host = os.environ["HOST"]
port = int(os.environ["PORT"])
version = os.environ["VERSION"]


@app.route("/")
def index():
    return render_template("index.pug", static="static", version=version)


if __name__ == "__main__":
    app.run(host=host, port=port, debug="DEBUG" in os.environ)