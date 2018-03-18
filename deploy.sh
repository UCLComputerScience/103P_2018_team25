#!/usr/bin/env bash

export STATIC_ROOT="$DEPLOYMENT_TARGET/static"

function python () {
  "/d/home/python364x64/python.exe" "$@"
}

echo "Installing requirements"

python -m pip install -r requirements.txt -q

echo "Collecting static files"

python ixn/manage.py collectstatic --noinput --clear

echo "Cleaning up deployment target"

rm -r $DEPLOYMENT_TARGET/ixn

echo "Running migrations"

python ixn/manage.py migrate

echo "Copying files to deployment target"

cp -R ixn $DEPLOYMENT_TARGET/
cp web.config $DEPLOYMENT_TARGET/
