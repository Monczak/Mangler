# The Mangler Text Generator

This is a microservice for analyzing text files and procedurally generating text using the information from those files. The service implements a REST API for accepting text generation requests and querying analysis/generation status.

The textgen is implemented as a Flask app with Celery for task management. This service runs on at least 3 Docker containers, being the Flask app, one or many Celery workers and one Celery beat, which schedules tasks. 
