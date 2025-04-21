import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from domains.models import Domain

class Command(BaseCommand):
    help = 'Import domains from a CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    domain_name = row['domain']
                    initial_date = datetime.strptime(row['creation_date'], '%Y-%m-%d').date() if row['creation_date'] else None
                    expiration_date = datetime.strptime(row['expiration_date'], '%Y-%m-%d').date() if row['expiration_date'] else None
                    lock_state = row['lock_state']
                    privacy = bool(int(row['privacy']))
                    status = row['status']
                    hosting_plan = row['hosting_plan']
                    ask_price = Decimal(row.get('ask_price', '0.0'))  # Convert to Decimal
                    compare_price = Decimal(row.get('compare_price', '0.0'))  # Convert to Decimal

                    domain, created = Domain.objects.update_or_create(
                        name=domain_name,
                        defaults={
                            'initial_date': initial_date,
                            'expiration_date': expiration_date,
                            'lock_state': lock_state,
                            'privacy': privacy,
                            'status': status,
                            'hosting_plan': hosting_plan,
                            'ask_price': ask_price,
                            'compare_price': compare_price,  # Include compare_price in defaults
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Domain "{domain_name}" created.'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Domain "{domain_name}" updated.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File "{csv_file}" not found.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))