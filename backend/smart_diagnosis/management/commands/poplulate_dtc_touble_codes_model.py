import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from smart_diagnosis.models import DtcTroubleCodes
from internal_users.models import InternalUser
import logging
import os

logger = logging.getLogger('managment_script')


class Command(BaseCommand):
    """
    Command for importing DTC codes from a CSV file into the DtcTroubleCodes model.

    Usage:
    python manage.py your_command_name path_to_csv_file
    """
    # Get the base name of the current script
    script_name = os.path.basename(__file__)
    help = "Imports DTC codes from a CSV file."

    def add_arguments(self, parser):
        """
        Adds command-line arguments.
        """
        parser.add_argument('csv_file', type=str,nargs='?', default='' help='Path to the CSV file.')

    def handle(self, *args, **kwargs):
        """
        Handle function to execute the command.
        """

        logger.info(f'starting management_script {self.script_name}...')
        print(f'starting management_script {self.script_name}...')
        
        csv_file_path = kwargs['csv_file']
        # Provide default path if no path given
        if not csv_file_path:
            csv_file_path = 'path/to/your/default/csv/file.csv'  # Please replace this with your actual default path
            logger.info(f"No csv_file_path provided. Using default path: {csv_file_path}")

        # Check if the file path is provided
        if not csv_file_path:
            raise CommandError('Please provide a valid CSV file path.')

        try:
            # Assuming a default user for created_by and updated_by fields. Default to user_id=3 (email=3333@gmail.com).

            default_user = InternalUser.objects.get(pk=3)
            print(
                f' internal_user ID and Name authorizing this script: {default_user.pk}:{default_user.user_first_name}')
            # If no default user found
            if not default_user:
                raise CommandError(
                    'Default user not found. Ensure InternalUser model has records.')

            with transaction.atomic():
                with open(csv_file_path, 'r') as file:
                    reader = csv.reader(file)
                    group_name = None
                    for row in reader:
                        # Check for empty rows or empty first column
                        if not row or not row[0]:
                            self.stderr.write(self.style.ERROR(
                                'Error: Empty row or empty DTC code detected.'))
                            continue

                        # Assuming the group name is in the first column
                        if "DTC Codes" in row[0]:
                            group_name = row[0]
                        else:
                            dtc_code = row[0]
                            dtc_description = row[1] if len(row) > 1 else None
                            DtcTroubleCodes.objects.create(
                                dtc_trouble_code=dtc_code,
                                dtc_trouble_code_description=dtc_description,
                                dtc_trouble_code_group_name=group_name,
                                created_by=default_user,
                                updated_by=default_user
                            )
                self.stdout.write(self.style.SUCCESS(
                    'Successfully imported DTC codes.'))

        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
