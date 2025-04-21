#!/bin/bash

echo "Make/Apply database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
EOF

# Start the Gunicorn server
echo "Starting Gunicorn..."
exec "$@"
