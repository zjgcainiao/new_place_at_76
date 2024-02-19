
# return the number of records that are affected by udpate() method.

from .base import models, VinNhtsaApiSnapshots,logger,get_object_or_404, aiohttp,transaction,json
from .database_sync_to_async import database_sync_to_async
from apis.api_vendor_urls import nhtsa_get_decoded_vin_extended_flat_format_url,nhtsa_get_safety_rating_by_vehicle_id_url, \
                            nhtsa_get_vehicle_id_url
from homepageapp.models import NhtsaSafetyRating, NhtsaDecodedVin,NhtsaVehicleId
from .fetch_and_save_nhtsa_decoded_vin import fetch_and_save_nhtsa_decoded_vin
from .fetch_and_save_nhtsa_vehicle_id import fetch_and_save_nhtsa_vehicle_id
    
# use the utility function `validate_field_mappings` to validate the field mappings
field_mappings = {
    "VehiclePicture": 'vehicle_picture_url',
      "OverallRating": "overall_rating",
      "OverallFrontCrashRating": "overall_front_crash_rating",
      "FrontCrashDriversideRating": "front_crash_drivers_side_rating",
      "FrontCrashPassengersideRating": "front_crash_passengers_side_rating",
      "FrontCrashPicture": "front_crash_picture_url",
      "FrontCrashVideo": "front_crash_video_url",
      "OverallSideCrashRating": "overall_side_crash_rating",
      "SideCrashDriversideRating": "side_crash_drivers_side_rating",
      "SideCrashPassengersideRating": "side_crash_passengers_side_rating",
      "SideCrashPicture": "side_crash_picture_url",
      "SideCrashVideo": "side_crash_video_url",
      "combinedSideBarrierAndPoleRating-Front": "combined_side_barrier_and_pole_rating_front",
      "combinedSideBarrierAndPoleRating-Rear": "combined_side_barrier_and_pole_rating_rear",
      "sideBarrierRating-Overall": "combined_side_barrier_rating_overall",
      "RolloverRating": "rollover_rating",
      "RolloverRating2": "rollover_rating_2",
      "RolloverPossibility": "rollover_possiblity",
      "RolloverPossibility2": "rollover_possiblity_2",
      "dynamicTipResult": "dynamic_tip_result",
      "SidePoleCrashRating": "side_pole_crash_rating",
      "SidePolePicture": "side_pole_picture_url",
      "SidePoleVideo": "side_pole_video_url",
      "NHTSAElectronicStabilityControl": "nhtsa_electronic_stability_control",
      "NHTSAForwardCollisionWarning": "nhtsa_forward_collision_warning",
      "NHTSALaneDepartureWarning": "nhtsa_lane_departure_warning",
      "ComplaintsCount": "complaints_count",
      "RecallsCount": "recalls_count",
      "InvestigationCount": "investigation_count",
      "ModelYear": "model_year",
      "Make": "make",
      "Model": "model",
      "VehicleDescription": "vehicle_description",
}

# @database_sync_to_async
async def fetch_and_save_nhtsa_safety_rating(vin):

    nhtsa_vin = await database_sync_to_async(get_object_or_404)(NhtsaDecodedVin, vin=vin)
    if not nhtsa_vin:
        nhtsa_vin,created, count,message = await fetch_and_save_nhtsa_decoded_vin(vin)
    
    make = nhtsa_vin.results['Make'].lower()
    model = nhtsa_vin.results['Model'].lower()
    model_year = nhtsa_vin.results['ModelYear'].lower()
    vehicle_ids_exsits = await database_sync_to_async(NhtsaVehicleId.objects.filter(make=make,model=model,model_year=model_year).exists)()
    if vehicle_ids_exsits:
        nhtsa_vehicle_ids = await database_sync_to_async(NhtsaVehicleId.objects.filter)(make=make,model=model,model_year=model_year)
    else:
        nhtsa_vehicle_ids = await fetch_and_save_nhtsa_vehicle_id(vin)
        if nhtsa_vehicle_ids:
            nhtsa_vehicle_ids = nhtsa_vehicle_ids[0] # retuns a tuple of nhtsa_vehicle_id_list and created_list,count and message


    nhtsa_safety_rating_list = []
    created_list = []
    nhtsa_vehicle_ids = await database_sync_to_async(list)(nhtsa_vehicle_ids)
    for nhtsa_vehicle_id in nhtsa_vehicle_ids:
        url = await database_sync_to_async(nhtsa_get_safety_rating_by_vehicle_id_url)(nhtsa_vehicle_id.vehicle_id)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

            # if no data, return an warning in the log
            if data is None:
                logger.warning(
                    f"No safety rating data returned for {vin}. Skipping further processing.")
                continue
            # Process and save the data as you do in your management script.
            # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
            count = data.get("Count", None)
            message = data.get("Message", "").strip() or None
            search_criteria = data.get("SearchCriteria", "").strip() or None

            results = data.get("Results")

            defaults = {}
            if isinstance(results, dict):
                for api_field, model_field in field_mappings.items():
                    if api_field in results:
                        defaults[model_field] = results.get(api_field)
            elif isinstance(results, list) and results:
                results = results[0]
                if isinstance(results, dict):
                    for api_field, model_field in field_mappings.items():
                        if api_field in results:
                            defaults[model_field] = results.get(api_field)
                            
                            nhtsa_safety_rating, created = await database_sync_to_async(
                                NhtsaSafetyRating.objects.update_or_create)(
                                    vin=vin,
                                    vehicle_id=nhtsa_vehicle_id,
                                    defaults=defaults,
                                )
                            nhtsa_safety_rating_list.append(nhtsa_safety_rating)
                            created_list.append(created)
                        
        except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
            logger.error(
                f"Failed to fetch extended vin info for {vin}. Error: {e}")
            # return None, None, None, None
        except Exception as e:
            logger.error(
            f"ailed to fetch extended vin info  for {vin}. Error: {e}")
    # return None, None, None, None
    return  nhtsa_safety_rating_list, created_list, count, message