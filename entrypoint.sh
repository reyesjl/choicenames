#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start the Gunicorn server
echo "Starting Gunicorn..."
exec "$@"
