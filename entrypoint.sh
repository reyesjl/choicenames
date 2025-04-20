#!/bin/bash

echo "Make/Apply database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Gunicorn server
echo "Starting Gunicorn..."
exec "$@"
