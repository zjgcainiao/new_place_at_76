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
from homepageapp.models import Inventories, PartsModel as Parts
from core_operations.utilities import clean_string_in_dictionary_object, convert_to_decimal, convert_to_boolean, convert_to_int, make_timezone_aware

from decimal import Decimal, InvalidOperation

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    """
    Django management command to populate the Inventory models.

    Attributes:
        help (str): Description of the command.
        module_dir (str): Directory path of the JSON data source.
        suffix_pattern (str): Suffix pattern of the JSON data source file.
        model_name (str): Model name for the data source.
    """

    help = 'popluate the Vendor, VendorLink, VendorAddresses,  data with the original data source file in json'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons/'
    suffix_pattern = '_20230115.json'
    model_name = 'Inventory'

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the command.

        This method reads the JSON data source and updates/creates vendor type records in the database.
        """
        start_time = time.time()  # Record the start time
        logger.info(f'starting management_script {self.script_name}...')
        print(f'starting management_script {self.script_name}...')

        parts_dict = {
            part_obj.part_id: part_obj for part_obj in Parts.objects.all()}

        file_path = os.path.join(
            self.module_dir, self.model_name + self.suffix_pattern)

        with open(file_path, 'r') as f:
            data = json.load(f)

            # try:
            with transaction.atomic():  # wrap in a transaction
                errors = []  # intial error list. empty.
                for entry in data:
                    primary_key_field = 'InventoryId'
                    if primary_key_field not in entry:
                        logging.error(
                            f"Skipping Inventory entry due to missing 'InventoryId': {entry}")
                        continue
                    # clean up empty strings in dictionary
                    entry = clean_string_in_dictionary_object(entry)
                    result = self.update_or_create_record(
                        entry, primary_key_field, parts_dict)
                    if result:
                        errors.append(result)
            if errors:
                self.stdout.write(self.style.ERROR('\n'.join(errors)))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'The {self.script_name} Script run successfully.'))

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        print(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")

    def update_or_create_record(self, entry, primary_key_field, parts_dict):

        inventory_id = entry.get(primary_key_field)

        # assigning inventory_part as a part_object
        part_id = entry.get('PartId') or None
        part_obj = parts_dict.get(part_id)
        total_cost = entry.get('TotalCost')
        last_cost = entry.get('LastCost')
        prior_to_last_cost = entry.get('PriorToLastCost')
        # print(
        #     f"here is the total_cost_amount: {total_cost} for Inventory ID {inventory_id}. Type is Decimal?:{isinstance(entry.get('TotalCost'), Decimal)}. Type {type(total_cost)}")
        # print(
        #     f"here is the last_cost_amount: {last_cost} for Inventory ID {inventory_id}")
        # use update_or_create
        defaults = {
            'inventory_part': part_obj,
            'inventory_on_hand': entry.get('OnHand') or None,
            'inventory_on_order': entry.get('OnOrder') or None,
            'inventory_location': entry.get('Location') or None,
            'inventory_last_sold_at': make_timezone_aware(entry.get('LastSold')),
            'inventory_committed_quantity': entry.get('CommittedQty') or None,
            'inventory_available_quantity': entry.get('AvailableQty') or None,
            'ivnentory_condition_id': entry.get('ConditionId') or None,
            'inventory_superceded_by': entry.get('SupercededBy') or None,
            'inventory_restock_quantity': entry.get('RestockQty') or None,
            'inventory_order_point': entry.get('OrderPoint') or None,
            'inventory_core_quantity': convert_to_decimal(entry.get('CoreQty')),
            'inventory_does_pay_comission': convert_to_boolean(entry.get('PayCommission')),
            'inventory_total_cost_amount': convert_to_decimal(total_cost),
            'inventory_last_cost_amount': convert_to_decimal(last_cost),
            'inventory_prior_to_last_cost_amount': convert_to_decimal(prior_to_last_cost),

        }

        try:
            inventory, created = Inventories.objects.update_or_create(
                inventory_id=inventory_id,
                defaults=defaults,
            )
            inventory.full_clean()
            inventory.save()
            print(
                f'inventory {inventory_id} record has been udapted. is_created?: {created}')
        except Exception as e:
            error_msg = f"An error occurred while updating/creating an Inventory record with ID {inventory_id}: {e}"
            logger.error(error_msg)
            print(error_msg)
            return error_msg
        return None
