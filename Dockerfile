FROM python:3.9-buster

RUN mkdir -p /app/backend
WORKDIR /app/backend

RUN apt-get update -y && apt-get install -y default-mysql-client default-libmysqlclient-dev

COPY ./backend/requirements.txt /app/backend
COPY ./backend/wheelhouse /app/backend/wheelhouse

RUN pip install -r requirements.txt -f wheelhouse

COPY ./backend /app/backend

# Augment the default search path for module files
ENV PYTHONPATH=/app/
