#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi

#python manage.py shell <<EOF
#from django.contrib.auth.models import User
#User.objects.create_superuser('admin', 'admin@example.com', '1234')
#EOF