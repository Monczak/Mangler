from celery import Celery

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task(bind=True)
def generate_text_task(self, input_files):
    generated_text = " ".join(input_files)

    with open("/usr/src/mangler/shared/generated_text.txt", "w") as file:
        file.write(generated_text)

    return {"result": "success"}