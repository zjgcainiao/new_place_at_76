
import asyncio
import json
import aiohttp
from django.db import models
from asgiref.sync import sync_to_async
from django.db import close_old_connections, DatabaseError, IntegrityError
from homepageapp.models import LicensePlateSnapShotsPlate2Vin
from homepageapp.models import VinNhtsaApiSnapshots, NhtsaVariableList
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES
# from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api
from asgiref.sync import sync_to_async
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

        except DatabaseError as de:
            # You can log the exception, take corrective actions or re-raise
            # For now, I'm just re-raising
            raise de

        except IntegrityError as ie:
            # Handle integrity errors, e.g., unique constraint violations
            # Again, you can log, correct or re-raise
            raise ie
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

    return VinNhtsaApiSnapshots.objects.filter(vin=vin).update(
        version=models.F('version') - 1
    )


@database_sync_to_async
def update_or_create_vin_snapshots_async(vin, variable, data):
    # grab the variable_instance from the lookup table NhtasVariableList model.

    # variable_instance, _ = NhtsaVariableList.objects.get_or_create(
    #     variable_id=variable_id)
    return VinNhtsaApiSnapshots.objects.update_or_create(
        vin=vin,
        variable=variable,
        defaults=data,
    )


async def fetch_latest_vin_data_from_snapshots(vin, group_names_list=POPULAR_NHTSA_GROUP_NAMES):
    # List of variable IDs to filter
    variable_ids_list = POPULAR_NHTSA_VARIABLE_IDS

    print('running async function `fetch_latest_vin_data_from_snapshots(vin)` to fetch vin info. pouplar fields only ')

    if not sync_to_async(VinNhtsaApiSnapshots.objects.filter(vin=vin).exists, thread_sensitive=True)():
        # VIN does not exist, so fetch and save the VIN data
        # Ensure the fetch_and_save_single_vin_from_nhtsa_api is an async function or properly awaited if using sync_to_async
        # await fetch_and_save_single_vin_from_nhtsa_api(vin)
        pass
# Include a join on the related NhtsaVariableList table and filter on the variable_group_name
    return sync_to_async(VinNhtsaApiSnapshots.objects.filter)(
        vin=vin,
        version=5,
        variable__variable_id__in=variable_ids_list,
        variable__variable_group_name__in=group_names_list,  # Filtering by group names
    ).select_related('variable').order_by('-created_at', 'vin', 'variable')


@database_sync_to_async
def fetch_latest_plate_data_from_snapshots(plate, state_abbr):
    return LicensePlateSnapShotsPlate2Vin.objects.filter(
        license_plate=plate,
        state=state_abbr,
    )
