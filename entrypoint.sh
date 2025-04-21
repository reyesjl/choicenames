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
for _ in range(100):
    ask_price = fake.pydecimal(left_digits=2, right_digits=2, positive=True)  # 0-99.99
    if fake.boolean(chance_of_getting_true=20):  # 20% chance for higher prices
        ask_price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)  # 100-999.99
    Domain.objects.create(
        name=fake.domain_name(),
        ask_price=ask_price,
        compare_price=ask_price + fake.pydecimal(left_digits=1, right_digits=2, positive=True)  # Slightly higher
    )
EOF

# Start the Gunicorn server
echo "Starting Gunicorn..."
exec "$@"
