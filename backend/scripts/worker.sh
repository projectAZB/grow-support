#!/usr/bin/env bash

set -x

if [[ $FLASK_ENV == "development" ]]
then
  watchmedo auto-restart --directory=/app/backend --pattern=*.py --recursive -- celery -A app.celery_worker.celery worker -l INFO
  exit
fi

celery -A app.celery_worker.celery worker -l INFO
