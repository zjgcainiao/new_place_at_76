# API utility function. modified in Dec 2023.
from re import search
from .base import models, now,  logging, NHTSA_API_URL, \
    UndefinedValueError, VinNhtsaApiSnapshots, \
    clean_string_in_dictionary_object, aiohttp, NhtsaVariableList, sync_to_async
from shops.models import Vin
from apis.api_vendor_urls import nhtsa_get_decoded_vin_extended_url
from .database_sync_to_async import database_sync_to_async
from django.http import JsonResponse
# from .decrement_version_for_vin_async import decrement_version_for_vin_async
# from .update_or_create_vin_snapshots_async import update_or_create_vin_snapshots_async

logger = logging.getLogger('external_api')


async def fetch_and_save_single_vin_from_nhtsa_api(vin, year=None):

    url = nhtsa_get_decoded_vin_extended_url(vin, year)

    logger.info(
        f'Initiating an api request to { NHTSA_API_URL}.')
    vin_snapshot_list = []
    # Fetch the Vin object corresponding to the vin
    vin_model, vin_created = await sync_to_async(Vin.objects.update_or_create,
                                                 thread_sensitive=True)(vin=vin)
    logger.info(f'vin_model {vin_model} is created ?:{vin_created}.')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

    except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
        logger.error(
            f"Failed to fetch VIN data for {vin} and model year {year}. Error: {e}")
        return None, None, None
    except Exception as e:
        logger.error(
            f"Failed to process and save VIN data for {vin} and model year {year}. Error: {e}")
        return None, None, None

    try:
        # if no data, return an warning in the log
        if not data or not data.get("Results"):
            logger.warning(
                f"No data returned for VIN {vin} and model year {year}. Skipping further processing.")
            return
        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip() or None

        results = data.get("Results")

        if results:
            logger.info(
                f"succesfully retrieving nhtsa records for vin {vin} and model year {year}.")

        for item in results:
            item = clean_string_in_dictionary_object(item)

            # Check the value of Value
            value = item.get("Value", None)

            # Ensure that value_id is a number, otherwise default to None
            try:
                value_id = int(item.get("ValueId") or 0)
                if value_id == 0:
                    value_id = None
            except ValueError:
                value_id = None

            # Check the value of Variable_name
            variable_name = item.get("Variable", None)
            if variable_name:
                variable_name = variable_name.strip() or None

            variable = None  # Default to None if no valid variable is found
            variable_id = item.get("VariableId")

            # Try to convert VariableId to an integer, if it's not None or empty
            if variable_id:
                try:
                    variable_id = int(variable_id)
                    # Fetch the NhtsaVariableList object corresponding to variable_id
                    variable, variable_created = await sync_to_async(NhtsaVariableList.objects.get_or_create,
                                                                     thread_sensitive=True
                                                                     )(variable_id=variable_id)
                    # logger.info(f'variable is {variable}....{variable.variable_name}')
                except Exception as e:
                    # If conversion to an integer fails or the variable_id does not exist, leave variable as None
                    logger.error(f'Failed to fetch variable \
                                 for variable_id {variable_id}...{e}')
                    variable = None
                    pass

            organized_data = {
                'results_count': count,
                'results_message': message,
                'results_search_criteria': search_criteria,

                "variable_name": variable_name,
                "value": value,
                "value_id": value_id,
                "source": NHTSA_API_URL,
            }

            # updated 2023-11-02 after variable_id becomes a foreign key field
            # variable=variable, override
            # vin_snapshot, created = await update_or_create_vin_snapshots_async(vin=vin, variable=variable, data=organized_data)

            # updated on 2023-12-24: async function, to create or update in VinNhtsaApiSnapshots model.
            vin_snapshot, created = await sync_to_async(
                VinNhtsaApiSnapshots.objects.update_or_create,
                thread_sensitive=True)(
                vin=vin_model,
                variable=variable,
                defaults=organized_data,
            )
            # if created:
            #     logger.info(f'saving new vin snapshots....')
            # else:
            #     logger.info(f'updating existing vin snapshots...{vin_snapshot}')
            vin_snapshot_list.append(vin_snapshot)

        logger.info(
            f'A list of nthsa records has been saved for {vin} and model year {year}..')
        logger.info(
            'fetch_sand_save_single_vin_from_nhtsa_api function is completed.')
        # return the data, the number of records downgraded, and if new records are created in the VinNhtsaSnapshots
        return vin_snapshot_list, search_criteria, message

    except ValueError as e:
        logger.error(
            f"Failed to process VIN {vin} (year: {year}). Invalid data format. Error: {e}")
        return JsonResponse({"error": "Invalid VIN format. Please check and try again."}, status=400)

    except KeyError as e:
        logger.error(
            f"VIN data for {vin} is missing a required field: {e}. Please contact support.")
        return JsonResponse({"error": "Error processing VIN data. Please contact support."}, status=500)

    except Exception as e:  # Catch-all for truly unexpected errors
        logger.critical(f"Unexpected error processing VIN {vin}: {e}")
        return JsonResponse({"error": "An unexpected error occurred. Please contact support."}, status=500)
