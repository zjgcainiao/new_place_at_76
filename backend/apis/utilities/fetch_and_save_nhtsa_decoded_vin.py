
# return the number of records that are affected by udpate() method.

from .base import models, VinNhtsaApiSnapshots, logger, get_object_or_404, aiohttp
from .database_sync_to_async import database_sync_to_async
from apis.api_vendor_urls import nhtsa_get_decoded_vin_extended_flat_format_url
from homepageapp.models import NhtsaDecodedVin
import json
import asyncio
# @database_sync_to_async


async def fetch_and_save_nhtsa_decoded_vin(vin, year=None):
    url = nhtsa_get_decoded_vin_extended_flat_format_url(vin, year)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        # if no data, return an warning in the log
        if data is None:
            logger.warning(
                f"No data returned for {vin}. Skipping further processing.")
            return
        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip() or None

        results = data.get("Results")
        if isinstance(results, list) and results:
            logger.info(
                f"result fetched successful for vin {vin} and {year}.")

            results = results[0]

        # Check if the first object is a dictionary
        if isinstance(results, dict):
            results = results
        else:
            logger.warning(
                f'the results is not a dictionary for {vin} and {year}')
            raise ValueError(
                f'the results is not a dictionary for {vin} and {year}')

        nhtsa_decoded_vin, created = await database_sync_to_async(
            NhtsaDecodedVin.objects.update_or_create)(
                vin=vin,
                defaults={
                    'results': results,
                    'count': count,
                    'message': message,
                    'search_criteria': search_criteria,
                    'url': url,
                }
        )
        return nhtsa_decoded_vin, created, count, message
    except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
        logger.error(
            f"Failed to fetch extended vin info for {vin}. Error: {e}")
        return None, None, None, None
    except Exception as e:
        logger.error(
            f"ailed to fetch extended vin info  for {vin}. Error: {e}")
        return None, None, None, None
