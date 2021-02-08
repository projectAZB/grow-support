#!/usr/bin/env bash

set -ex

cd /app/backend

alembic upgrade head
