#!/bin/bash

chown -R nobody:nogroup $ROOT

celery -A tasks.celery worker \
       --loglevel=info \
       --uid=nobody --gid=nogroup