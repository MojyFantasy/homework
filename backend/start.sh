#!/bin/bash
python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
python manage.py init&&
uwsgi --ini /var/www/html/backend/uwsgi.ini
