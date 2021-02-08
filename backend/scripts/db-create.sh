#!/usr/bin/env bash

set -ex

mysql --host="$MYSQL_HOST" \
      --port="$MYSQL_PORT" \
      -u"$MYSQL_USER" \
      -p"$MYSQL_PASSWORD" \
      -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DBNAME"
