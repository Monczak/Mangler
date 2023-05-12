import os

from pathlib import Path
from time import time

from celery import Celery

from common.configloader import parse_toml, ConfigError
from common.logger import get_logger
from schema import BackendConfigSchema

logger = get_logger()

UPLOADS_PATH = os.environ["UPLOADS"]
GENERATED_PATH = os.environ["GENERATED"]

CONFIG_PATH = "backend.toml"
try:
    config = parse_toml(CONFIG_PATH, BackendConfigSchema())
    logger.info("Config loaded successfully")
except ConfigError as err:
    logger.error(str(err))
    exit(1)

celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])
celery.config_from_object("celeryconfig")

###########################
# Task-specific functions #
###########################


def cleanup(path, min_lifetime):
    count = 0

    for file_path in Path(path).glob("*"):
        if not file_path.is_file():
            continue

        if time() - file_path.stat().st_mtime < min_lifetime:
            continue

        else:
            file_path.unlink()
            count += 1

    if count > 0:
        logger.info(f"Deleted {count} file{'s' if count != 1 else ''}")



#########
# Tasks #
#########


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        config["cleanup"]["uploads_cleanup_interval"],
        cleanup_uploads_task,
        name="cleanup uploads"
    )
    
    sender.add_periodic_task(
        config["cleanup"]["generated_cleanup_interval"],
        cleanup_generated_task,
        name="cleanup generated files"
    )


@celery.task(bind=True, queue="backend")
def cleanup_uploads_task(self):
    cleanup(UPLOADS_PATH, config["cleanup"]["uploads_min_lifetime"])


@celery.task(bind=True, queue="backend")
def cleanup_generated_task(self):
    cleanup(GENERATED_PATH, config["cleanup"]["generated_min_lifetime"])
