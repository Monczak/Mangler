#!/bin/bash

chown -R nobody:nogroup $ROOT

celery -A tasks.celery beat \
       --loglevel=info \
       --uid=nobody --gid=nogroup