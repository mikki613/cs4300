#!/usr/bin/env bash
set -o errexit

# Install dependencies (Render often does this automatically,
# but leaving it here is okay if your service isn't auto-installing)
pip install -r requirements.txt

# Database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Optional: create superuser if env var says so
python scripts/create_superuser.py
