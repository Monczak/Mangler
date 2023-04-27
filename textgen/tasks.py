import logging
import os

from pathlib import Path

from celery import Celery, states
from celery.exceptions import Ignore

from generator.textgen import TextGenerator, TextgenError

celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])
textgen = TextGenerator(os.environ["UPLOADS"], os.environ["CACHE"])


class TaskFailure(Exception):
    pass


@celery.task(bind=True)
def generate_text_task(self, input_id, depth, seed, length):
    try:
        freq_dict = textgen.analyze(input_id, [depth])
        generator = textgen.make_generator(seed, freq_dict, depth)

        buffer_size = 1024
        chars_left = length

        with open(Path(os.environ["GENERATED"]) / input_id, "w") as file:
            while chars_left > 0:
                buffer = "".join([next(generator) for _ in range(min(chars_left, buffer_size))])
                file.write(buffer)
                chars_left -= len(buffer)

        return {"result": "success"}
    except Exception as err:
        logging.warning(str(err))
        raise TaskFailure(err)
    