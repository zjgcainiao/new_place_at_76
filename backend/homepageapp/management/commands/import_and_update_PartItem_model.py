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
from homepageapp.models import PartItemModel
from core_operations.common_functions import clean_string_in_dictionary_object
from core_operations.utilities import parse_to_two_digit_decimal

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    """
    Django management command to populate the PartItem models.

    Attributes:
        help (str): Description of the command.
        module_dir (str): Directory path of the JSON data source.
        suffix_pattern (str): Suffix pattern of the JSON data source file.
        model_name (str): Model name for the data source.
    """

    help = 'popluate the Vendor, VendorLink, VendorAddresses,  data with the original data source file in json'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons/'
    suffix_pattern = '_20230115.json'
    model_name = 'PartItem'
    primary_key_field = 'PartItemId'
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
        print(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")

    def update_or_create_record(self, entry, primary_key_field):

        part_item_id = entry.get(primary_key_field)

        # use update_or_create
        defaults = {
            'line_item_id' : entry.get('LineItemId') or None,
            'part_discount_description_id' : entry.get('PartDiscountDescriptionId') or None,
            'part_item_is_user_entered_unit_sale' : entry.get('IsUserEnteredUnitSale') or None,
            'part_item_is_user_entered_unit_cost' : entry.get('IsUserEnteredUnitCost') or None,
            'part_item_quantity' : parse_to_two_digit_decimal(entry.get('Quantity')),
            'part_item_unit_price' : parse_to_two_digit_decimal(entry.get('UnitPrice')),
            'part_item_unit_list' : parse_to_two_digit_decimal(entry.get('UnitList')),
            'part_item_unit_sale' : parse_to_two_digit_decimal(entry.get('UnitSale')),
            'part_item_unit_cost' : parse_to_two_digit_decimal(entry.get('UnitCost')),
            'part_item_part_no' : entry.get('PartNo') or None,
            'part_item_part_id' : entry.get('PartId') or None,
            'part_item_is_confirmed' : entry.get('IsConfirmed') or  False,
            'part_item_vendor_code' : entry.get('VendorCode') or None,
            'part_item_vendor_id' : entry.get('VendorId') or None,
            'part_item_manufacture_id' : entry.get('ManufacturerId') or None,
            'part_item_invoice_number' : entry.get('InvoiceNumber') or None,
            'part_item_commission_amount' : entry.get('CommissionAmount') or None,
            'part_item_is_committed' : entry.get('IsCommitted') or False,
            'part_item_is_quantity_confirmed' : entry.get('IsQuantityConfirmed')  or False,
            'part_item_confirmed_quantity' :  parse_to_two_digit_decimal(entry.get('ConfirmedQuantity')),
            'part_item_is_part_ordered' : entry.get('IsPartOrdered') or False,
            'part_item_is_core' : entry.get('IsCore') or False,
            'part_item_is_bundled_kit' : entry.get('IsBundledKit') or None,
            'part_item_is_MPlg_item' : entry.get('IsMPlgItem') or False,
            'part_item_is_changed_MPlg_item' : entry.get('IsChangedMPlgItem') or None,
            'part_item_part_type' : entry.get('PartType') or None,
            'part_item_size' : entry.get('Size') or None,
            'part_item_is_tire' : entry.get('IsTire') or  False,
            'part_item_vendor_id' : entry.get('CatalogVendorId') or None,
            'part_item_last_updated_date' : entry.get('LastChangeDate') or None,
            'part_item_meta' : entry.get('Metadata') or None,
            'part_item_added_from_supplier' : entry.get('AddedFromSupplier') or None,
            'part_item_purchased_from_vendor' : entry.get('PurchasedFromVendor') or None,
            'part_item_purchased_from_supplier' : entry.get('PurchasedFromSupplier') or None,
            'part_item_shipping_description' : entry.get('ShippingDescription') or None,
            'part_item_shipping_cost' :  parse_to_two_digit_decimal(entry.get('ShippingCost')),
        }

        try:
            part_item, created = PartItemModel.objects.update_or_create(
                part_item_id=part_item_id,
                defaults=defaults,
            )
            part_item.full_clean()
            part_item.save()
            logger.info(
                f'Part Item {part_item_id} record has been updated. is_created?: {created}.')
            print(
                f'Part Item {part_item_id} record has been updated. is_created?: {created}.')
        except Exception as e:
            error_msg = f"An error occurred while updating/creating a {self.model_name} record {part_item_id}: {e}"
            logger.error(error_msg)
            # print(error_msg)
            # debugging; pause when there is an error
            logger.info(f"{entry.get('UnitPrice')} of {self.model_name}  {part_item_id}")
            # pause the script 
            # pause the script
            input("Error(s) occurred while running this script. Press enter to continue.")
            return error_msg
        return None
