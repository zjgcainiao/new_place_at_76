"""
Module for updating or creating vendor information in the database.

This module provides the management command `import_and_update_vendors_model`
to populate the Vendor, VendorLink, VendorAddresses models from a JSON data source.

Attributes:
    logger (Logger): Logger instance for logging management script activities.

Classes:
    Command(BaseCommand): Django management command for updating/creating vendor information.
"""
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
from homepageapp.models import NoteItemsNewSQL02Model
from core_operations.utilities import clean_string_in_dictionary_object
from core_operations.utilities import parse_to_two_digit_decimal

logger = logging.getLogger('management_script')


class Command(BaseCommand):
  

    help = 'populate and update NoteItem with the original data source file in json'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons/'
    suffix_pattern = '_20230115.json'
    model_name = 'NoteItem'
    primary_key_field = 'NoteItemId'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the JSON data source and updates/creates vendor type records in the database.
        """
        start_time = time.time()  # Record the start time
        logger.info(f'starting management script {self.script_name}...')


        file_path = os.path.join(
            self.module_dir, self.model_name + self.suffix_pattern)

        with open(file_path, 'r') as f:
            data = json.load(f)

            # data = clean_string_in_dictionary_object(data)
            # try:
            with transaction.atomic():  # wrap in a transaction
                errors = []  # intial error list. empty.
                for entry in data:
                    primary_key_field = self.primary_key_field or None
                    if primary_key_field not in entry:
                        logging.error(
                            f"Skipping {self.model_name} entry due to missing '{primary_key_field}': {entry}")
                        continue
                    # clean up empty strings in dictionary
                    entry = clean_string_in_dictionary_object(entry)
                    result = self.update_or_create_record(
                        entry, primary_key_field)
                    if result:
                        errors.append(result)
            if errors:
                self.stdout.write(self.style.ERROR('\n'.join(errors)))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Script {self.script_name} runs successfully.'))

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")


    def update_or_create_record(self, entry, primary_key_field):

        note_item_id = entry.get(primary_key_field)

        # use update_or_create
        defaults = {
            'line_item_id' : entry.get('LineItemId') or None,
            'note_item_text' : entry.get('NoteText') or None,
            'note_item_is_printed_on_order' : entry.get('PrintOnOrder') or False,
            'note_item_tech_observation' : entry.get('TechObservation') or None,
        }

        try:
            note_item, created = NoteItemsNewSQL02Model.objects.update_or_create(
                note_item_id=note_item_id,
                defaults=defaults,
            )
            note_item.full_clean()
            note_item.save()
            logger.info(
                f'{self.model_name} {note_item_id} record has been updated. is_created?: {created}.')

        except Exception as e:
            error_msg = f"An error occurred while updating/creating a {self.model_name} record {note_item_id}: {e}"
            logger.error(error_msg)
            # print(error_msg)
            # debugging; pause when there is an error
            logger.info(f"{entry.get('UnitPrice')} of {self.model_name} {note_item_id}")
            # pause the script 
            input("Error(s) occurred while running this script. Press enter to continue.")
            return error_msg
        return None
