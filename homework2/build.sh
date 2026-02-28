#!/usr/bin/env bash
set -o errexit

echo "==== RUNNING build.sh ===="
python --version
pwd
ls -la

python manage.py migrate
python manage.py collectstatic --noinput

echo "==== TRYING TO CREATE SUPERUSER ===="
python bookings/create_superuser.py
echo "==== FINISHED SUPERUSER STEP ====" 
