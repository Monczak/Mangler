import logging
import os

from pathlib import Path

from celery import Celery, states
from celery.exceptions import Ignore

from cachemanager import CacheManager
from generator.textgen import TextGenerator, TextgenError
from generator.freqdict import FreqDictSerializer


logger = logging.getLogger("mangler")


celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])
textgen = TextGenerator(os.environ["UPLOADS"])
cache_manager = CacheManager(os.environ["CACHE"], os.environ["REDIS_URL"])


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

        logger.info(f"Generating {length} characters for {input_id}")
        generator = textgen.make_generator(seed, freq_dict, gen_depth)

        buffer_size = 1024
        chars_generated = 0

        with open(Path(os.environ["GENERATED"]) / input_id, "w") as file:
            while chars_generated < length:
                # buffer = [None] * min(chars_left, buffer_size)
                # for i in range(len(buffer)):
                #     buffer[i] = generator.next
                #     self.update_state(state="PROGRESS", meta={"current": generator.count, "total": length})

                buffer = "".join([generator.next for _ in range(min(length - chars_generated, buffer_size))])
                file.write(buffer)
                chars_generated += len(buffer)
                self.update_state(state="PROGRESS", meta={"current": chars_generated, "total": length})

        return {"result": "success"}
    except (FileNotFoundError, TextgenError) as err:
        logger.warning(str(err))
        raise Ignore()
    except Exception as err:
        logger.error(str(err))
        raise TaskFailure(err)
    