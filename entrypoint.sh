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

# Generate 50 fake domain names
python manage.py shell <<EOF
from faker import Faker
from domains.models import Domain
fake = Faker()
for _ in range(50):
    Domain.objects.create(
        name=fake.domain_name(),
        ask_price=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
        compare_price=fake.pydecimal(left_digits=5, right_digits=2, positive=True)
    )
EOF

# Start the Gunicorn server
echo "Starting Gunicorn..."
exec "$@"
