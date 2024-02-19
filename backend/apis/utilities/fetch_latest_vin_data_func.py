from .base import models, POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES, \
    VinNhtsaApiSnapshots, NhtsaVariableList, logger, \
    sync_to_async
from .fetch_and_save_single_vin_from_nhtsa_api import fetch_and_save_single_vin_from_nhtsa_api
from .get_vin_snapshot_queryset import get_vin_snapshot_queryset
from .database_sync_to_async import database_sync_to_async


async def fetch_latest_vin_data_func(vin, 
                                     variable_ids_list=POPULAR_NHTSA_VARIABLE_IDS, 
                                     group_names_list=POPULAR_NHTSA_GROUP_NAMES):


    # List of variable IDs to filter
    variable_ids_list = POPULAR_NHTSA_VARIABLE_IDS

    logger.info('initiating async function `fetch_latest_vin_data_func` to fetch vin info. pouplar fields only. ')

    # Convert the synchronous exists() call to an async call using sync_to_async and await it
    vin_exists = await sync_to_async(VinNhtsaApiSnapshots.objects.filter(vin=vin).exists, thread_sensitive=True)()
    logger.info(f'checking if vin {vin} records exist in database...')

    if not vin_exists:
        # VIN does not exist, so fetch and save the VIN data
        # Ensure the fetch_and_save_single_vin_from_nhtsa_api is an async function or properly awaited if using sync_to_async
        await fetch_and_save_single_vin_from_nhtsa_api(vin)

    # Includes a join on the related NhtsaVariableList table and filter on the variable_group_name
    # Now retrieve the filtered records asynchronously
    queryset = await sync_to_async(
        get_vin_snapshot_queryset, 
        thread_sensitive=True)(vin)

    return queryset
