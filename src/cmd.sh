#!/usr/bin/env sh
set -ex
python wait-for-database.py
python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py makemigrations website
python manage.py migrate website
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000