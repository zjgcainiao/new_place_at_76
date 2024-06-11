import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from customer_users.models import CustomerUser
from django.db import transaction
import os
from faker import Faker
import logging
import time
logger = logging.getLogger('management_script')

class Command(BaseCommand):
    help = 'Sets customer_users passwords from a given CSV file.'
    csv_base_folder = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/my-development-notes-2023/deployment_toolkits/dummy_user_data/'
    file_name = '2024_04_07_dummy_customer_user_list.csv'
    default_csv_path = os.path.join(csv_base_folder, file_name)
    # start time
    start_time = time.time()

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
            self.stdout.write(self.style.ERROR(
                f"CSV file does not exist at path: {csv_file_path}"))
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
                        user, created = CustomerUser.objects.get_or_create(
                            cust_user_email=email)
                        if created:
                            # Set random first and last name using Faker
                            user.cust_user_first_name = faker.first_name()
                            user.cust_user_middle_name = faker.first_name()
                            user.cust_user_last_name = faker.last_name()
                            # user.cust_user_phone_number = faker.phone_number()
                        # Set the password and save the user instance
                        user.set_password(password)
                        user.save()
                        action = "created" if created else "updated"
                        affected_users.append({
                            'email': email,
                            'first_name': user.cust_user_first_name,
                            'middle_name': user.cust_user_middle_name,
                            'last_name': user.cust_user_last_name,
                            # 'phone_number': user.cust_user_phone_number,
                            'action': action,
                        })

                        logger.info(f"Password {action} for {email}")

                except IntegrityError as e:
                    logger.error(f"Error updating password for {email}: {e}")

                except Exception as e:
                    logger.error(
                        f"An unexpected error occurred for {email}: {e}")

        # Generate the output file name based on the current date
        output_file_name = datetime.now().strftime(
            "%Y_%m_%d") + "_affected_customer_users.csv"
        output_file_path = os.path.join(self.csv_base_folder, output_file_name)
        # Write affected users to the new CSV file
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['email', 'first_name',
                          'middle_name', 'last_name', 'action']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in affected_users:
                writer.writerow(user)

        logger.error(f"Affected customer users have been written to {output_file_path}")
        # end time
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.stdout.write(self.style.SUCCESS(f"The script took {elapsed_time:>5.2f} seconds to run."))
