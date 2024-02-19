
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
from homepageapp.models import CannedJobLineItemSequence,CannedJobsNewSQL02Model,LineItemsNewSQL02Model
from core_operations.common_functions import clean_string_in_dictionary_object
from core_operations.utilities import parse_to_two_digit_decimal

logger = logging.getLogger('management_script')


class Command(BaseCommand):


    help = 'popluate the CannedJobLineItemSequence data with the original data source file in json.'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons/'
    suffix_pattern = '_20230115.json'
    model_name = 'CannedJobLineItemSequence'
    primary_key_field = 'CannedJobLineItemSequenceId'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    # prefetch canned_job_dict and line_item_dict
    canned_job_dict = {canned_job.canned_job_id: canned_job for canned_job in CannedJobsNewSQL02Model.objects.all()}
    line_item_dict = {line_item.line_item_id: line_item for line_item in LineItemsNewSQL02Model.objects.all()}

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the JSON data source and updates/creates vendor type records in the database.
        """
        start_time = time.time()  # Record the start time
        logger.info(f'starting management script {self.script_name}...')
        print(f'starting management script {self.script_name}...')

        file_path = os.path.join(
            self.module_dir, self.model_name + self.suffix_pattern)



        with open(file_path, 'r') as f:
            data = json.load(f)

            # data = clean_string_in_dictionary_object(data)
            # try:
            with transaction.atomic():  # wrap in a transaction
                errors = []  # intial error list. empty.
                for entry in data:
                    primary_key_field = self.primary_key_field
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
        print(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")

    def update_or_create_record(self, entry, primary_key_field):

        id = entry.get(primary_key_field)

        # Retrieve objects from stored dictionaries instead of DB queries
        canned_job_obj = self.canned_job_dict.get(entry.get('CannedJobId')) or None
        line_item_obj = self.line_item_dict.get(entry.get('LineItem')) or None

        # use update_or_create
        defaults = {
            'canned_job' :canned_job_obj,
            'line_item' : line_item_obj,
            'sequence': entry.get('Sequence') or None
        }
        try:
            sequence_item, created = CannedJobLineItemSequence.objects.update_or_create(
                id=id,
                defaults=defaults,
            )
            sequence_item.full_clean()
            sequence_item.save()
            logger.info(
                f'{self.model_name} {id} record has been updated. is_created?: {created}.')

        except Exception as e:
            error_msg = f"An error occurred while updating/creating a {self.model_name} record {id}: {e}"
            logger.error(error_msg)
            # print(error_msg)
            # pause the script
            input("Error(s) occurred while running this script. Press enter to continue.")
            return error_msg
        return None
