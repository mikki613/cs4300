#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

# static files for whitenoise
python manage.py collectstatic --noinput