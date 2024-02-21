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
from we_handle_money_stuff.models import GLSubAccountType
from core_operations.utilities import clean_string_in_dictionary_object

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = 'popluate the sub_gl_account_type data with the original data source file in csv file.'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/my-development-notes-2023/deployment_toolkits/initial_data/'
    file_name ='2024_02_01_gl_sub_account_type_initial_data.csv'

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
                    # clean up empty strings in dictionary

                    for entry in data:
                        entry = clean_string_in_dictionary_object(entry)
                        name = entry.get('name') or None
                        if not name:
                            logger.error(
                                f"Skipping record due to missing 'name' field: {entry}")
                            continue

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

        try:
            gl_sub_account_type, created = GLSubAccountType.objects.update_or_create(
                                name=name,
                                defaults=entry,
            )
            if created:
                logger.info(f'Created new GLSubAccountType: {gl_sub_account_type.name}')
            else:
                logger.info(f'Updated GLSubAccountType: {gl_sub_account_type.name}')
            gl_sub_account_type.full_clean()
            gl_sub_account_type.save()
            logger.info(
                f'GL Account Name {gl_sub_account_type.name} record has been updated. is_created?: {created}.')
        except ValidationError as e:
            self.errors.append(f"Validation error for {name}: {e}")
        except Exception as e:
            error_msg = f"An error occurred while updating/creating an gl_sub_account_type record with sub_account_number {name}: {e}"
            logger.error(error_msg)
            # print(error_msg)
            return error_msg
        return None
