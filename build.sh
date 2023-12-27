#!/usr/bin/env bash
# exit on error
set -o errexit

#rm .whitenoise_manifest.json
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --clear --no-input --traceback
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations chat
python manage.py migrate chat
#if [[ $CREATE_SUPERUSER ]];
#then
#  python manage.py createsuperuser --no-input
#fi
