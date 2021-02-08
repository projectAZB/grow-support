#!/usr/bin/env bash

if [[ $# -ne 1 ]]
then
  echo "One string denoting table to be cleared is needed."
  exit 1
fi

mysql --host="$MYSQL_HOST" \
      --port="$MYSQL_PORT" \
      -u"$MYSQL_USER" \
      -p"$MYSQL_PASSWORD" \
      -e"USE $MYSQL_DBNAME; DELETE FROM $1"
