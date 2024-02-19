
# return the number of records that are affected by udpate() method.

from .base import logger,get_object_or_404, aiohttp
from .database_sync_to_async import database_sync_to_async
from apis.api_vendor_urls import nhtsa_get_decoded_vin_extended_flat_format_url,nhtsa_get_safety_rating_by_vehicle_id_url,nhtsa_get_vehicle_id_url
from homepageapp.models import NhtsaDecodedVin, NhtsaVehicleId
from .fetch_and_save_nhtsa_decoded_vin import fetch_and_save_nhtsa_decoded_vin
# @database_sync_to_async
async def fetch_and_save_nhtsa_vehicle_id(vin):

    nhtsa_vin = await database_sync_to_async(get_object_or_404)(NhtsaDecodedVin, vin=vin)
    nhtsa_vehicle_id_list = []
    created_list = []
    if not nhtsa_vin:
        nhtsa_vin,created, count,message = await fetch_and_save_nhtsa_decoded_vin(vin)
    else:
        make=nhtsa_vin.results['Make'].lower()
        model=nhtsa_vin.results['Model'].lower()
        year=nhtsa_vin.results['ModelYear'].lower()
        vehicle_id_url = nhtsa_get_vehicle_id_url(make,model,year)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(vehicle_id_url) as response:
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

            if results:
                logger.info(
                    f"result fetched successful for vin {vin} and {year}.")
            for result in results:
                vehicle_id=result.get('VehicleId')
                if not vehicle_id:
                    raise ValueError('VehicleId is not found in the results.')
                    
                vehicle_description=result.get('VehicleDescription')
                nhtsa_vehicle_id, created = await database_sync_to_async(
                    NhtsaVehicleId.objects.update_or_create)(
                        vehicle_id=vehicle_id,
                        defaults={
                            'make': make,
                            'model': model,
                            'model_year': year,
                            'vehicle_description': vehicle_description,
                            }
                    )
                nhtsa_vehicle_id_list.append(nhtsa_vehicle_id)
                created_list.append(created)
            return nhtsa_vehicle_id_list, created_list, count, message
        except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
            logger.error(
                f"Failed to fetch extended vin info for {vin}. Error: {e}")
            return None, None, None, None
        except Exception as e:
            logger.error(
                f"ailed to fetch extended vin info  for {vin}. Error: {e}")
            return None, None, None, None
