import os

from pathlib import Path

from celery import Celery

celery = Celery(__name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])

@celery.task
def generate_text_task(input_id):
    generated_text = input_id

    with open(Path(os.environ["GENERATED"]) / "generated_text.txt", "w") as file:
        file.write(generated_text)

    return {"result": "success"}