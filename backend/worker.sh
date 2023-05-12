#!/bin/bash

chown -R nobody:nogroup $ROOT

celery -A tasks.celery worker \
       -Q backend \
       --loglevel=info \
       --uid=nobody --gid=nogroup