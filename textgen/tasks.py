import os

from pathlib import Path

from celery import Celery

from generator.textgen import TextGenerator

celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])

@celery.task
def generate_text_task(input_id, depth, seed, length):
    # TODO: Rework this to support separated logic for handling files
    textgen = TextGenerator(os.environ["UPLOADS"], os.environ["CACHE"])
    freq_dict = textgen.analyze(input_id, [depth])
    generator = textgen.make_generator(seed, freq_dict, depth)

    buffer_size = 1024
    chars_left = length

    with open(Path(os.environ["GENERATED"]) / "generated_text.txt", "w") as file:
        while chars_left > 0:
            buffer = "".join([next(generator) for _ in range(min(chars_left, buffer_size))])
            file.write(buffer)
            chars_left -= buffer_size

    return {"result": "success"}