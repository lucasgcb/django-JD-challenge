#!/usr/bin/env bash
echo "Running migrations!"
python manage.py makemigrations jungle_api
python manage.py migrate auth
python manage.py migrate
echo "Recreating django super user now..."
echo "from django.contrib.auth.models import User; import os; User.objects.filter(username=os.environ['WEB_ADMIN_NAME']).delete(); User.objects.create_superuser(os.environ['WEB_ADMIN_NAME'], os.environ['WEB_ADMIN_EMAIL'], os.environ['WEB_ADMIN_PW'])" | python manage.py shell

if [ ! -d "./jungle_code/static-django" ]; then
	echo "Deploying static django files..."
	python manage.py collectstatic --noinput
fi

if [ $PYSVR = "1" ]; then
	python manage.py runserver 0.0.0.0:8000 
else
	gunicorn --bind=0.0.0.0 jungle_code.wsgi
fi
