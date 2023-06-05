# The Mangler Backend

This is the Python backend for The Mangler. It serves the frontend and implements a REST API for accepting text generation requests.

The backend runs on a Flask server and uses Celery for task management. It is tightly integrated with the textgen microservice, extends its API with more functionality and makes it available to users.
