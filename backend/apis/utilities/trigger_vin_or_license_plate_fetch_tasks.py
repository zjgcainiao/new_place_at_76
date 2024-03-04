
from .fetch_single_plate_data_via_plate2vin_api import  \
    fetch_single_plate_data_via_plate2vin_api
from .fetch_and_save_nhtsa_decoded_vin import fetch_and_save_nhtsa_decoded_vin
from .create_or_update_vin_record import create_or_update_vin_record
from .database_sync_to_async import database_sync_to_async
from .fetch_and_save_nhtsa_recalls import fetch_and_save_nhtsa_recalls
from .fetch_and_save_nhtsa_safety_rating import \
    fetch_and_save_nhtsa_safety_rating
from .fetch_and_save_nhtsa_vehicle_id import fetch_and_save_nhtsa_vehicle_id
from .base import logger
from django.db import transaction
import asyncio
from asgiref.sync import sync_to_async
from django.db import IntegrityError
from aiohttp import ClientError, ClientResponseError, ClientConnectionError
from django.core.exceptions import ObjectDoesNotExist

# Path: backend/apis/utilities/fetch_single_plate_data_via_plate2vin_api.py

# task to trigger vin or license plate fetch tasks


async def trigger_vin_or_license_plate_fetch_tasks(vin=None,
                                                   license_plate=None,
                                                   state=None):
    try:
        if license_plate and state:
            logger.info(
                'license_plate and state are provided. fetching new data via api vendors.')
            plate_data, _ = await \
                fetch_single_plate_data_via_plate2vin_api(license_plate, state)
            if not plate_data or not plate_data.vin:
                logger.error(
                    'No associated vin found for the license plate and state. Skipping further processing.')
                return

            vin = plate_data.vin

        if vin:
            # Ensuring create_or_update_vin_record is an async function
            await create_or_update_vin_record(vin)
            # Run fetch operations concurrently
            tasks = [
                fetch_and_save_nhtsa_decoded_vin(vin),
                fetch_and_save_nhtsa_recalls(vin),
                fetch_and_save_nhtsa_safety_rating(vin),
                fetch_and_save_nhtsa_vehicle_id(vin)
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):  # Check for failed tasks
                    logger.error(f"Task failed: {result}")
                    # Decide if you want to raise an error and stop processing here
    except ObjectDoesNotExist:
        logger.error(
            f"No NhtsaDecodedVin matches the given query for vin: {vin}")
        return None, False
    except (asyncio.TimeoutError) as e:
        logger.error(f"Timeout error occurred: {e}")
        return None, False
    except (ClientError) as e:
        logger.error(f"Client-side error occurred: {e}")
        return None, False
    except Exception as e:
        # Catch-all for any other unexpected issues
        logger.error(
            f'Unexpected error in trigger_vin_or_license_plate_fetch_tasks: {str(e)}')
        raise e
    return vin, True
