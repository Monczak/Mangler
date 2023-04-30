import logging
import os

from pathlib import Path

from celery import Celery, states
from celery.exceptions import Ignore

from cachemanager import CacheManager, CacheLockedError
from generator.textgen import TextGenerator, TextgenError, StuckError
from generator.freqdict import FreqDictSerializer


logger = logging.getLogger("mangler")


celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])
textgen = TextGenerator(os.environ["UPLOADS"])
cache_manager = CacheManager(os.environ["CACHE"], os.environ["REDIS_URL"])


CACHE_LOCKED_RETRY_TIME = 5
CACHE_LOCKED_RETRY_MAX_ATTEMPTS = 5


class TaskFailure(Exception):
    pass


@celery.task(bind=True)
def generate_text_task(self, input_id, train_depths, gen_depth, seed, length):
    try:
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

        buffer_size = 1024
        max_gen_retries = 10
        current_attempt = -1

        logger.info(f"Generating {length} characters for {input_id}")
        while True:
            generator = textgen.make_generator(seed, freq_dict, gen_depth)
            current_attempt += 1
            if current_attempt >= max_gen_retries:
                return {"result": "failed"}     # TODO: Better error message

            with open(Path(os.environ["GENERATED"]) / input_id, "w") as file:
                try:
                    while generator.count < length:
                        buffer = "".join([generator.next for _ in range(min(length - generator.count, buffer_size))])
                        file.write(buffer)
                        self.update_state(state="PROGRESS", meta={"current": generator.count, "total": length})
                except StuckError as err:
                    logger.warning(f"Generator got stuck at pos {generator.count} ({repr(err.previous)}|{repr(err.current)}), retrying ({current_attempt + 1}/{max_gen_retries})")
                    continue
            
            break

        return {"result": "success"}    # TODO: Better success message
    except CacheLockedError as err:
        logger.warning(f"Cache for {err.file_name} is in use by another task, retrying in {CACHE_LOCKED_RETRY_TIME} seconds")
        raise self.retry(exc=err, countdown=CACHE_LOCKED_RETRY_TIME, max_retries=CACHE_LOCKED_RETRY_MAX_ATTEMPTS)
    except (FileNotFoundError, TextgenError) as err:
        logger.warning(str(err))
        raise Ignore()
    except Exception as err:
        logger.error(str(err))
        raise TaskFailure(err)
    