
import asyncio
import json
import aiohttp
from django.db import models
from asgiref.sync import sync_to_async
from django.db import close_old_connections
from homepageapp.models import LicensePlateSnapShotsPlate2Vin
from homepageapp.models import VinNhtsaAPISnapshots

# from core_operations.common_functions import clean_string_in_dictionary_object
# import logging


# this is a custom version of sync_to_async function that explcitly control database connections
# 1. manages the connection's lifecycle expliclty, ensure that connections are properly closed afer usage.
# 2. i can add logiging speicifc to database operations.
# 3. can cutomize common database exceptions uniformly.


def database_sync_to_async(func):
    """
    Turn a sync function that interacts with the database into an async function.
    Handles database connection management and common exception handling.
    """

    @sync_to_async
    def wrapper(*args, **kwargs):
        try:
            # Ensure old DB connections are closed
            close_old_connections()
            # Execute the function
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Handle common database exceptions if required.
            # For example: handle DatabaseError, IntegrityError, etc.
            # You can log the exception or take other corrective actions.
            raise e
        finally:
            # Ensure old DB connections are closed after function execution
            close_old_connections()

    return wrapper

# return the number of records that are affected by udpate() method.


@database_sync_to_async
def decrement_version_for_vin_async(vin):

    return VinNhtsaAPISnapshots.objects.filter(vin=vin).update(
        version=models.F('version') - 1
    )


@database_sync_to_async
def update_or_create_vin_snapshots_async(vin, variable_id, data):
    return VinNhtsaAPISnapshots.objects.update_or_create(
        vin=vin,
        variable_id=variable_id,
        defaults=data,
    )


@database_sync_to_async
def fetch_latest_vin_data_from_snapshots(vin):
    # List of variable IDs to filter
    variable_ids_list = [5, 10, 11, 20]

    return VinNhtsaAPISnapshots.objects.filter(
        vin=vin,
        version=5,
        variable_id__in=variable_ids_list,
    ).ordered_by('-created_at', 'variable_id')
