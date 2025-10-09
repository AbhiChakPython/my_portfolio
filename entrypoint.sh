#!/bin/bash

# 1. Run Setup Commands
# Collect static files
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Running migrations..."
python manage.py migrate

# 2. Start the Gunicorn Web Process
# The 'exec' command replaces the current shell with Gunicorn, ensuring it's the main process.
echo "Starting Gunicorn web server..."
exec gunicorn myportfolio.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 60