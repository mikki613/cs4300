#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

#  Run migrations on deploy
python manage.py migrate --noinput

#  Static files for whitenoise
python manage.py collectstatic --noinput