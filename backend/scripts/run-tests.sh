#!/usr/bin/env bash

set -e

export TESTING=True

mysql --host="$MYSQL_HOST" \
      --port="$MYSQL_PORT" \
      -u"$MYSQL_USER" \
      -p"$MYSQL_PASSWORD" \
      -e "CREATE DATABASE IF NOT EXISTS $MYSQL_TEST_DBNAME"

alembic upgrade head

pytest "$@"

mysql --host="$MYSQL_HOST" \
      --port="$MYSQL_PORT" \
      -u"$MYSQL_USER" \
      -p"$MYSQL_PASSWORD" \
      -e "DROP DATABASE IF EXISTS $MYSQL_TEST_DBNAME"
