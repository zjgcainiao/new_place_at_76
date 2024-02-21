

import time
import json
import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from django.db import transaction
from django.core.management.base import BaseCommand
from homepageapp.models import NhtsaServiceBulletin
from core_operations.utilities import clean_string_in_dictionary_object
from core_operations.utilities import parse_to_two_digit_decimal
import csv

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    """
    Django management command to populate the NhtsaServiceBulletin model.


    """

    help = 'popluate the NhtsaServiceBulletin json'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/nhtsa_data/'
    file_name = 'flat_tsbs.txt'
    model_name = 'NhtsaServiceBulletin'
    # primary_key_field = ''
    # Define a mapping of input data fields to Django model fields. there are no field headers in the flat_tsb.txt file
    field_mapping = {
        0: 'bul_no',
        1: 'bul_rep',
        2: 'nhtsa_item_number',
        3: 'bul_date',
        4: 'complaint_name',
        5: 'make_txt',
        6: 'model_txt',
        7: 'year_txt',
        8: 'date_added',
        9: 'summary',
    }
    unique_together_fields_indices = [7, 5, 6, 2] # ['YEARTXT','MAKETEXT','MODELTEXT','ID']

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the JSON data source and updates/creates vendor type records in the database.
        """
        start_time = time.time()  # Record the start time
        logger.info(f'starting management script {self.script_name}...')
        print(f'starting management script {self.script_name}...')

        file_path = os.path.join(
            self.module_dir, self.file_name)

        with open(file_path, 'r') as f:
            while True:
                # Read a block of data
                block = list(csv.reader(f, delimiter='\t', chunksize=50000))  # Adjust chunk size as needed
                
                # Break the loop if there's no more data
                if not block:
                    break
                
                # Process each entry in the block
                with transaction.atomic():
                    errors = []
                    for entry in block:
                        result = self.update_or_create_record(entry)
                        if result:
                            errors.append(result)
                if errors:
                    logger.error(f"Errors encountered: {errors}")
                    self.stdout.write(self.style.ERROR('\n'.join(errors)))
                else:
                    logger.info(
                        f'Script {self.script_name} runs successfully.')
                    self.stdout.write(self.style.SUCCESS(
                        f'Script {self.script_name} runs successfully.'))

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")

    def update_or_create_record(self,entry):
        try: 
            # Dynamically construct the lookup dict for update_or_create
            # Prepare the record using field_mapping
            
            defaults = {model_field: entry[idx] if idx < len(entry) and entry else None 
            for idx, model_field in self.field_mapping.items() if idx not in self.unique_together_fields_indices}

            # Example of adding a default value for a missing field
            lookup_dict = {model_field: entry[idx] for idx, model_field in self.field_mapping.items() if idx in self.unique_together_fields_indices}

            # Add or update the record in the database
            nthsa_service_bulletin, created = NhtsaServiceBulletin.objects.update_or_create(**lookup_dict, defaults=defaults)
            nthsa_service_bulletin.full_clean()
            nthsa_service_bulletin.save()
            logger.info(
                f'{self.model_name} {nthsa_service_bulletin.nhtsa_item_number} record for \
                    {nthsa_service_bulletin.year_txt} {nthsa_service_bulletin.make_txt} {nthsa_service_bulletin.model_txt} has been updated. is_created?: {created}.')

        except Exception as e:
            error_msg = f"An error occurred while updating/creating a {self.model_name} record. {e}"
            logger.error(error_msg, exc_info=True)
            # print(error_msg)
            # pause the script 
            input("Error(s) occurred while running this script. Press control + C to exit...Press enter to continue...")
            return error_msg
        return None
    