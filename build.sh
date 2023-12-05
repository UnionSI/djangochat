#!/usr/bin/env bash
# exit on error
set -o errexit

#rm .whitenoise_manifest.json
rm -r staticfiles
pip install -r requirements.txt
python manage.py collectstatic --clear --no-input
python manage.py makemigrations
python manage.py makemigrations room
python manage.py migrate room

