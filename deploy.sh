#!/usr/bin/env bash

function python () {
  "/d/home/python364x64/python.exe" "$@"
}

echo "Installing requirements"

python -m pip install -r requirements.txt -q

echo "Collecting static files"

python manage.py collectstatic --noinput

echo "Cleaning up deployment target"

rm -r $DEPLOYMENT_TARGET/ixn
rm -r $DEPLOYMENT_TARGET/static

echo "Running migrations"

python manage.py migrate

echo "Creating default superuser"

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@ixn.org.uk', 'admin')"

echo "Copying files to deployment target"

cp -R ixn $DEPLOYMENT_TARGET/
cp -R ixn_auth $DEPLOYMENT_TARGET/
cp -R matchingsystem $DEPLOYMENT_TARGET/
cp -R static $DEPLOYMENT_TARGET/
cp web.config $DEPLOYMENT_TARGET/
