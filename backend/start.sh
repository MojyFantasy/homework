#!/bin/bash
python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
uwsgi --ini /var/www/html/backend/uwsgi.ini