
import asyncio
import json
import aiohttp
from django.db import models
from asgiref.sync import sync_to_async
from django.db import close_old_connections, DatabaseError, IntegrityError
from homepageapp.models import LicensePlateSnapShotsPlate2Vin
from homepageapp.models import VinNhtsaApiSnapshots, NhtsaVariableList

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


@database_sync_to_async
def fetch_latest_vin_data_from_snapshots(vin):
    # List of variable IDs to filter
    variable_ids_list = [25, 26, 27, 28, 29, 34, 38, 39, 5, 37, 63,
                         9, 11, 12, 13, 17, 18, 21, 24, 62, 64, 66, 67, 71, 122, 125,
                         # 126, 129 defines the value of electric vehicle motor info.
                         126, 129,
                         ]

    print('running function fetch_latest_vin_data_from_snapshots(vin) to fetch vin info ')
    return VinNhtsaApiSnapshots.objects.filter(
        vin=vin,
        version=5,
        variable_id__in=variable_ids_list,
    ).order_by('-created_at', 'variable')


@database_sync_to_async
def fetch_latest_plate_data_from_snapshots(plate, state_abbr):
    return LicensePlateSnapShotsPlate2Vin.objects.filter(
        license_plate=plate,
        state=state_abbr,
    )
