from common.logger import setup_logger, get_logger
setup_logger()
logger = get_logger()

import os

from pathlib import Path

from flask import Flask, render_template

from schema import BackendConfigSchema
from common.configloader import ConfigError, parse_toml

frontend_path = Path(os.environ["FRONTEND"])

CONFIG_PATH = "backend.toml"
try:
    config = parse_toml(CONFIG_PATH, BackendConfigSchema())
    logger.info("Config loaded successfully")
except ConfigError as err:
    logger.error(str(err))
    exit(1)

app = Flask(__name__, static_folder=frontend_path / "static", template_folder=frontend_path / "templates")
app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

app.config["MAX_CONTENT_SIZE"] = config["file_limits"]["max_file_size"]

import api

with app.app_context():
    app.register_blueprint(api.api, url_prefix="/api")

host = os.environ["HOST"]
port = int(os.environ["PORT"])
version = os.environ["VERSION"]


@app.route("/")
def index():
    return render_template("index.pug", static="static", version=version)


if __name__ == "__main__":
    app.run(host=host, port=port, debug="DEBUG" in os.environ)