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
from we_handle_money_stuff.models import  GLSubAccount, GLAccount
from core_operations.common_functions import clean_string_in_dictionary_object

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = 'popluate the sub_gl_account data with the original data source file in csv file.'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/my-development-notes-2023/deployment_toolkits/initial_data/'
    file_name ='2024_02_01_gl_sub_account_initial_data.csv'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the csv data source and create/update the initial data for the gl sub account records in the database.
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
                        # clean up empty strings in dictionary
                        entry = clean_string_in_dictionary_object(entry)
                        sub_account_number = entry.pop('sub_account_number',None) 
                        parent_account_name = entry.pop('parent_account', None)
                        parent_account = None
                        if parent_account_name:
                            try:
                                parent_account = GLAccount.objects.get(name=parent_account_name)
                            except GLAccount.DoesNotExist:
                                errors.append(f"Parent GL account not found for name: {parent_account_name}")
                                continue
                        
                        if not sub_account_number:
                            logger.error(
                                f"Skipping record due to missing 'sub_account_number' field: {entry}")
                            continue
                        
                        # Replace entry.parent_account with the parent_account instance
                        entry['parent_account'] = parent_account

                        result = self.update_or_create_record(
                            entry, sub_account_number)
                        
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

    def update_or_create_record(self, entry, sub_account_number):
        try:
            gl_sub_account, created = GLSubAccount.objects.update_or_create(
                                sub_account_number=sub_account_number,
                                defaults=entry,
            )
            if created:
                logger.info(f'Created new GLSubAccount: {gl_sub_account.name}')
            else:
                logger.info(f'Updated GLSubAccount: {gl_sub_account.name}')
            gl_sub_account.full_clean()
            gl_sub_account.save()
            logger.info(
                f'GL Sub Account Name {gl_sub_account.name}_sub_acct_number_{sub_account_number} record has been udapted. is_created?: {created}.')
        except ValidationError as e:
            self.errors.append(f"Validation error for {sub_account_number}: {e}")
        except Exception as e:
            error_msg = f"An error occurred while updating/creating an gl_sub_account record with sub_account_number {sub_account_number}: {e}"
            logger.error(error_msg)
            # print(error_msg)
            return error_msg
        return None
