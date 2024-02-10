import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from internal_users.models import InternalUser
from django.db import transaction
import os
from faker import Faker

# Assuming your InternalUser model is the default user model
# User = get_user_model()
User = InternalUser
class Command(BaseCommand):
    help = 'Sets user passwords from a given CSV file.'
    default_csv_path = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/my-development-notes-2023/deployment_toolkits/automatic_scripts/database_related/dummy_user_data/2024_01_16_dummy_internal_user_list.csv'


    def add_arguments(self, parser):
        parser.add_argument(
            '-csv', '--csv_file', 
            type=str, 
            help='The CSV file path', 
            default=self.default_csv_path
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        faker = Faker()
        affected_users = []
        # Check if the CSV file exists
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file does not exist at path: {csv_file_path}"))
            return

        # Read and process the CSV file
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                email = row['email'].strip()
                password = row['password'].strip()

                # Enclose the user update in a transaction for atomicity
                try:
                    with transaction.atomic():
                        # Retrieve the user by email
                        user, created = InternalUser.objects.get_or_create(email=email)
                        if created:
                            # Set random first and last name using Faker
                            user.user_first_name = faker.first_name()
                            user.user_last_name = faker.last_name()
                        # Set the password and save the user instance
                        user.set_password(password)
                        user.save()
                        affected_users.append({
                                                'email': email,
                                                'first_name': user.user_first_name,
                                                'last_name': user.user_last_name,
                                                'created': created
                                                })

                        action = "created" if created else "updated"
                        self.stdout.write(self.style.SUCCESS(f"Password {action} for {email}"))

                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Error updating password for {email}: {e}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"An unexpected error occurred for {email}: {e}"))
        
        # Generate the output file name based on the current date
        output_file_name = datetime.now().strftime("%y%m%d") + "_affected_internal_users.csv"
        
        # Write affected users to the new CSV file
        with open(output_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['email', 'first_name', 'last_name', 'created']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in affected_users:
                writer.writerow(user)

        self.stdout.write(self.style.SUCCESS(f"Affected users have been written to {output_file_name}"))