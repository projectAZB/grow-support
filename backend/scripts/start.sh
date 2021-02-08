#!/usr/bin/env bash

# access-logfile: `-` signifies stdout
# error-logfile: `-` signifies stderr

gunicorn -w 1 --bind :5000 \
    --reload \
    --access-logformat \
    '{"logger":"gunicorn","host":"%(h)s","code":"%(s)s","method":"%(m)s","path":"%(U)s","query":"%(q)s","size":"%(B)s"}' \
    --access-logfile - \
    --error-logfile - \
    --log-level=info \
    wsgi:app
