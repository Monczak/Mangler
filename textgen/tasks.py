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
def generate_text_task(self, input_id, train_depths, gen_depth, seed, length):
    try:
        # TODO: Handle concurrent requests for the same input id - so they don't clash when dealing with the input id's cache
        freq_dict = textgen.load_cache(input_id)
        if not freq_dict or not freq_dict.supports(train_depths, gen_depth):
            logging.info(f"Creating new freqdict for {input_id}")
            freq_dict = textgen.analyze(input_id, train_depths)

            logging.info(f"Caching {freq_dict.name}")
            textgen.save_cache(freq_dict)
        else:
            logging.info(f"Using cached freqdict for {input_id}")

        generator = textgen.make_generator(seed, freq_dict, gen_depth)

        buffer_size = 1024
        chars_left = length

        with open(Path(os.environ["GENERATED"]) / input_id, "w") as file:
            while chars_left > 0:
                buffer = [None] * min(chars_left, buffer_size)
                for i in range(len(buffer)):
                    buffer[i] = generator.next
                    self.update_state(state="PROGRESS", meta={"current": generator.count, "total": length})
                
                file.write("".join(buffer))
                chars_left -= len(buffer)

        return {"result": "success"}
    except (FileNotFoundError, TextgenError) as err:
        logging.warning(str(err))
        raise Ignore()
    except Exception as err:
        logging.error(str(err))
        raise TaskFailure(err)
    