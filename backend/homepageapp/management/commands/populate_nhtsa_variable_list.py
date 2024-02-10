from django.core.management.base import BaseCommand, CommandError
import requests
from homepageapp.models import NhtsaVariableList
import logging
import os
import time
from datetime import datetime
from django.db import transaction

URL = "https://vpic.nhtsa.dot.gov/api/vehicles/getvehiclevariablelist?format=json"

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    """
    Management command to fetch data from the NHTSA API and populate the NhtsaVariableList model.

    Usage:
        python manage.py populate_nhtsa_variable_list
    """
    help = 'Fetches data from the NHTSA API and populates the NhtsaVariableList model'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **options):

        start_time = time.time()  # Record the start time

        logger.info(f'starting management_script {self.script_name}...')
        print(f'starting management_script {self.script_name}...')

        try:
            # Setting a timeout to prevent indefinite waiting
            response = requests.get(URL, timeout=20)

            # Check if the request was successful
            response.raise_for_status()

            data = response.json()

            if 'Results' not in data:
                raise CommandError(
                    'Invalid response format from the NHTSA API.')

            with transaction.atomic():  # Begin transaction block
                for item in data['Results']:
                    NhtsaVariableList.objects.update_or_create(
                        variable_id=item.get("ID", None),
                        defaults={
                            'variable_name': item.get("Name", None),
                            'variable_group_name': item.get("GroupName", None),

                            'variable_description_html': item.get("Description", None),

                            'variable_data_type': item.get("DataType", None)
                        }
                    )

            self.stdout.write(self.style.SUCCESS(
                'Successfully populated the NhtsaVariableList model.'))

        except requests.RequestException as e:
            raise CommandError(f"Network error: {e}")

        except ValueError:  # This will catch JSON decoding errors among others
            raise CommandError("Error parsing the response from the NHTSA API")

        except Exception as e:
            raise CommandError(f"Unexpected error occurred: {e}")

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        print(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
