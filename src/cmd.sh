#!/usr/bin/env sh
set -ex
if [ "${DJANGO_SETTINGS_MODULE}" ==  "app.settings.production" ]; then
  python wait-for-database.py
fi
python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py makemigrations website
python manage.py migrate website
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000