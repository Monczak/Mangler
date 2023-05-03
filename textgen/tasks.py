import os
import uuid

from enum import Enum
from pathlib import Path

from celery import Celery
from celery.exceptions import Ignore, SoftTimeLimitExceeded

from cachemanager import CacheManager, CacheLockedError
from configloader import parse_toml, ConfigError
from generator.textgen import TextGenerator, TextgenError, StuckError, DepthError, SeedLengthError, BadSeedError
from generator.freqdict import FreqDictSerializer
from logger import get_logger
from schema import TextgenConfigSchema


logger = get_logger()


CONFIG_PATH = "textgen.toml"
try:
    config = parse_toml(CONFIG_PATH, TextgenConfigSchema())
    logger.info("Config loaded successfully")
except ConfigError as err:
    logger.error(str(err))
    exit(1)


celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])
textgen = TextGenerator(os.environ["UPLOADS"])
cache_manager = CacheManager(os.environ["CACHE"], os.environ["REDIS_URL"])


class Errors(Enum):
    MAX_RETRIES_EXCEEDED = {"code": 10, "reason": "max retries exceeded"}
    BAD_SEED = {"code": 11, "reason": "bad seed"}
    BAD_SEED_LENGTH = {"code": 12, "reason": "invalid seed length"}
    INVALID_DEPTH = {"code": 13, "reason": "invalid depth"}
    INVALID_LENGTH = {"code": 14, "reason": "invalid length"}
    BAD_DEPTH = {"code": 15, "reason": "bad depth"}

    TIMEOUT = {"code": 98, "reason": "timeout"}

    INTERNAL = {"code": 99, "reason": "internal"}


class TextgenTaskResult:
    @staticmethod
    def success(**kwargs):
        return {"result": "success", **kwargs}
    
    @staticmethod
    def failure(error=None, **kwargs):
        return {"result": "failed", **(error.value), **kwargs}


class TaskFailure(Exception):
    pass


def get_result(task_id):
    return celery.AsyncResult(task_id)


@celery.task(bind=True, soft_time_limit=config["tasks"]["soft_time_limit"], time_limit=config["tasks"]["time_limit"])
def generate_text_task(self, input_id, train_depths, gen_depth, seed, length):
    """
    Generate text based on the contents of the files specified by input_id.
    Use cached data for text generation if available and usable.
    """

    def handle_failure(error, **kwargs):
        error_data = TextgenTaskResult.failure(error, **kwargs)
        return error_data

    try:
        # Some safety checks to ensure the task's args are nice and valid
        if any([depth > config["textgen"]["max_depth"] for depth in train_depths]) or gen_depth > config["textgen"]["max_depth"]:
            return handle_failure(Errors.INVALID_DEPTH)
        
        if length > config["textgen"]["max_length"]:
            return handle_failure(Errors.INVALID_LENGTH)
        
        if gen_depth not in train_depths:
            return handle_failure(Errors.BAD_DEPTH, details=f"Depth {gen_depth} is invalid, must be one of {set(train_depths)}")

        # Actually analyze and generate text
        with cache_manager.acquire(input_id, "r+b") as cache:
            serializer = FreqDictSerializer()

            freq_dict = None
            if cache.exists:
                freq_dict = serializer.deserialize(cache.file.read())
            
            if not freq_dict or not freq_dict.supports(train_depths, gen_depth):
                logger.info(f"Creating new freqdict for {input_id}")
                freq_dict = textgen.analyze(input_id, train_depths)

                logger.info(f"Caching {freq_dict.name}")
                cache.file.seek(0)
                cache.file.write(serializer.serialize(freq_dict))
            else:
                logger.info(f"Using cached freqdict for {input_id}")

        buffer_size = config["textgen"]["buffer_size"]
        max_gen_retries = config["textgen"]["max_gen_retries"]
        current_attempt = -1

        out_file_name = str(uuid.uuid4())

        logger.info(f"Generating {length} characters for {input_id}, outfile is {out_file_name}")
        while True:
            generator = textgen.make_generator(seed, freq_dict, gen_depth)
            current_attempt += 1
            if current_attempt >= max_gen_retries:
                return TextgenTaskResult.failure(Errors.MAX_RETRIES_EXCEEDED)

            with open(Path(os.environ["GENERATED"]) / out_file_name, "w") as file:
                try:
                    while generator.count < length:
                        buffer = "".join([generator.next for _ in range(min(length - generator.count, buffer_size))])
                        file.write(buffer)
                        self.update_state(state="GENERATING", meta={"current": generator.count, "total": length})
                except StuckError as err:
                    logger.warning(f"Generator got stuck at pos {generator.count} ({repr(err.previous)}|{repr(err.current)}), retrying ({current_attempt + 1}/{max_gen_retries})")
                    continue
                except Exception as err:
                    logger.error(f"Something went wrong with text generation: {str(err)}")
                    continue
            
            break

        return TextgenTaskResult.success(output_id=out_file_name)
    except CacheLockedError as err:
        logger.warning(f"Cache for {err.file_name} is in use by another task, retrying in {config['cache']['retry_delay']} seconds")
        raise self.retry(exc=err, countdown=config['cache']['retry_delay'], max_retries=config['cache']['cache_locked_retries'])
    except BadSeedError as err:
        return handle_failure(Errors.BAD_SEED, details=str(err))
    except SeedLengthError as err:
        return handle_failure(Errors.BAD_SEED_LENGTH, details=str(err))
    except DepthError as err:
        return handle_failure(Errors.BAD_DEPTH, details=str(err))
    except (FileNotFoundError, TextgenError) as err:
        logger.warning(str(err))
        raise Ignore()
    except SoftTimeLimitExceeded as err:
        # Do cleanup here
        return handle_failure(Errors.TIMEOUT)
    except Exception as err:
        logger.error(str(err))
        raise TaskFailure(err)
    