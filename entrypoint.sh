#!/bin/bash

# Define the production settings file
# Set DJANGO_SETTINGS_MODULE environment variable explicitly
export DJANGO_SETTINGS_MODULE='myportfolio.settings_prod'

# 1. Run Setup Commands (using production settings)
echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

# 2. Start the Gunicorn Web Process
echo "Starting Gunicorn web server with $DJANGO_SETTINGS_MODULE..."
exec gunicorn myportfolio.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 60
