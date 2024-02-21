import time
import json
import os
import csv
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.utils import timezone
import logging
from django.db import transaction
from django.core.management.base import BaseCommand
from we_handle_money_stuff.models import GLAccountType
from core_operations.utilities import clean_string_in_dictionary_object

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = 'popluate the gl_account_type data with the original data source file in csv file.'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/my-development-notes-2023/deployment_toolkits/initial_data/'
    file_name ='2024_02_01_gl_account_type_initial_data.csv'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the csv data source and create/update the initial data for the gl_account_type records in the database.
        """
        start_time = time.time()  # Record the start time
        logger.info(f'starting management script {self.script_name}...')
        # print(f'starting management script {self.script_name}...')

        file_path = os.path.join(
            self.module_dir, self.file_name)
        
        try:
            with open(file_path, 'r',encoding='utf-8-sig') as f:
                # data = json.load(f)
                data = csv.DictReader(f)
                # data = clean_string_in_dictionary_object(data)
                # try:
                with transaction.atomic():  # wrap in a transaction
                    errors = []  # intial error list. empty.
                    for entry in data:
                        # entry = clean_string_in_dictionary_object(entry)
                        name = entry.pop('name',None)
                        if not name:
                            logger.error(
                                f"Skipping record due to missing 'name' field: {entry}")
                            continue
                        # clean up empty strings in dictionary
                        result = self.update_or_create_record(
                            entry, name)
                        
                        # by default, there is no result returned, if result is not, it means there is an error
                        if result:
                            errors.append(result)
                if errors:
                    logger.error('\n'.join(errors))
                else:
                    logger.info(
                        f'Script {self.script_name} runs successfully.')

            # Compute the elapsed time
            elapsed_time = time.time() - start_time
            logger.info(
                f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        # print(
        #     f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        except FileNotFoundError:
                logger.error(f"File {self.file_name} not found.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        logger.info(f"Script finished in {time.time() - start_time} seconds.")

    def update_or_create_record(self, entry, name):
        # Clean the entry dictionary to only include valid field names for GLAccountType
        model_fields = [f.name for f in GLAccountType._meta.get_fields()]
        cleaned_entry = {k: v for k, v in entry.items() if k in model_fields and k}

        try:
            gl_account_type, created = GLAccountType.objects.update_or_create(
                name=name,
                defaults=cleaned_entry,  # Use the cleaned_entry with valid field names
            )
            gl_account_type.full_clean()  # Validate the model instance
            gl_account_type.save()  # Save the object to the database

            logger.info(
                f'GL Account Type {gl_account_type.name} record has been updated. is_created?: {created}.'
            )
        except ValidationError as e:
            self.errors.append(f"Validation error for {name}: {e}")
        except Exception as e:
            error_msg = f"An error occurred while updating/creating a GLAccountType record with name {name}: {e}"
            logger.error(error_msg)
            return error_msg
        return None
