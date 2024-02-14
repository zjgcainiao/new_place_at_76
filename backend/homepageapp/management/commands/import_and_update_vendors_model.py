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
from homepageapp.models import Vendors
from core_operations.common_functions import clean_string_in_dictionary_object

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    """
    Django management command to populate the  VendorLink models.

    Attributes:
        help (str): Description of the command.
        module_dir (str): Directory path of the JSON data source.
        suffix_pattern (str): Suffix pattern of the JSON data source file.
        model_name (str): Model name for the data source.
    """

    help = 'popluate the Vendor, VendorLink, VendorAddresses,  data with the original data source file in json'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons/'
    suffix_pattern = '_20230115.json'
    model_name = 'Vendor'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the JSON data source and updates/creates vendor records in the database.
        """
        start_time = time.time()  # Record the start time
        logger.info(f'starting management_script {self.script_name}...')

        file_path = os.path.join(
            self.module_dir, self.model_name + self.suffix_pattern)

        with open(file_path, 'r') as f:
            data = json.load(f)

            # data = clean_string_in_dictionary_object(data)
            # try:
            with transaction.atomic():  # wrap in a transaction
                errors = []  # intial error list. empty.
                for entry in data:
                    primary_key_field = 'VendorId'
                    if primary_key_field not in entry:
                        logging.error(
                            f"Skipping vendor entry due to missing 'VendorId': {entry}")
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
                    'The `import_and_update_vendors_model` Script run successfully.'))
        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")

        
    def update_or_create_record(self, entry, primary_key_field):
        # if 'VehicleId' not in entry:
        #     error_msg = f"Skipping entry due to missing 'VehicleId': {entry}"
        #     logging.error(error_msg)
        #     return error_msg

        vendor_id = entry.get(primary_key_field)
        vendor_type_obj = entry.get('VendorTypeId')
        vendor_catalog_link_obj = entry.get('CatalogLinkId')
        # use update_or_create
        defaults = {
            'vendor_name': entry.get('Name'),
            'vendor_contact_persons': entry.get('Contact'),
            'vendor_comment': entry.get('Comment'),
            'vendor_contact_email_address': entry.get('EmailAddress'),
            'vendor_code': entry.get('Code'),
            'vendor_limit': entry.get('Limit'),
            'vendor_terms': entry.get('Terms'),
            'vendor_account_class': entry.get('AcctClass'),
            'vendor_type': vendor_type_obj,
            'vendor_catalog_link': vendor_catalog_link_obj,
        }
        try:
            vendor, created = Vendors.objects.update_or_create(
                vendor_id=vendor_id,
                defaults=defaults,
            )
            vendor.full_clean()
            vendor.save()

        except Exception as e:
            error_msg = f"An error occurred while updating/creating a vendor with ID {vendor_id}: {e}"
            logger.error(error_msg)
            print(error_msg)
            return error_msg
        return None
