
# return the number of records that are affected by udpate() method.

from .base import models, VinNhtsaApiSnapshots,logger,get_object_or_404, aiohttp,transaction,json
from .database_sync_to_async import database_sync_to_async
from apis.api_vendor_urls import nhtsa_get_safety_rating_by_vehicle_id_url, \
                            nhtsa_get_vehicle_id_url, nhtsa_get_recalls_url
from homepageapp.models import NhtsaDecodedVin,NhtsaVehicleId
from homepageapp.models import NhtsaRecall
from .fetch_and_save_nhtsa_decoded_vin import fetch_and_save_nhtsa_decoded_vin
from .fetch_and_save_nhtsa_vehicle_id import fetch_and_save_nhtsa_vehicle_id
from datetime import datetime
# from django.shortcuts import get_object_or_404
# use the utility function `apis.utilities.validate_field_mappings` to validate the field mappings
# {'apis_field':'model_field'}
field_mappings = {
    "Manufacturer": "manufacturer",
    "NHTSACampaignNumber": "nhtsa_compaign_number",
    "parkIt": "park_it",
    "parkOutSide": "park_outside",
    "NHTSAActionNumber": "nhtsa_action_number",
    "ReportReceivedDate": "report_received_date",
    "Component": "recall_component",
    "Summary": "recall_summary",
    "Remedy": "recall_remedy",
    "Notes": "recall_notes",
    # critera for update_or_create
    "ModelYear": "model_year",
    "Make": "make",
    "Model": "model",
}

# @database_sync_to_async
async def fetch_and_save_nhtsa_recalls(vin):

    # incorrect way: recalls = await database_sync_to_async(Recall.objects.filter)(vin=vin)
    # recalls = await database_sync_to_async(list)(Recall.objects.filter(vin=vin))
    # if recalls:
    #     return recalls, False, None, "Existing records found"
    
    decoded_vin = await database_sync_to_async(get_object_or_404)(NhtsaDecodedVin, vin=vin)
    if not decoded_vin:
        decoded_vin,created, count,message = await fetch_and_save_nhtsa_decoded_vin(vin)
    
    try:
        make = str(decoded_vin.results['Make']).lower()
        model = str(decoded_vin.results['Model']).lower()
        model_year = str(decoded_vin.results['ModelYear']).lower()
    except (KeyError, AttributeError):
        # Handle the error here
        make = ""
        model = ""
        model_year = ""

    url = nhtsa_get_recalls_url(make, model, model_year)
    nhtsa_recall_list = []
    created_list = []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        # if no data, return an warning in the log
        if data is None:
            logger.warning(
                f"No recall info returned for {vin}. Skipping further processing.")
            # return None, None, None, None
        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip() or None

        results = data.get("results")
        if not results:
            results = data.get("Results")
            if not results:
                logger.warning(f"No recall info returned for {vin}. Skipping further processing.")
                input(f'Results is {results}. Press Ctrl+C to exit')
                return None, None, None, None
        
        defaults = {}
        # assume results in the data looks like results :[{},{},{}]
        if isinstance(results, list) and results:
            # assume results in the data looks like results :[{},{},{}]
            # in case of multiple recalls wrapped in a dict() list
            for recall in results:
                # print(f'here is the recall: {recall}')

                for api_field, model_field in field_mappings.items():
                    if api_field in recall:
                        value = recall.get(api_field)
                        # Check if the field name suggests it's a date field
                        if "date" in model_field.lower():
                            try:
                                # Attempt to parse the date
                                # Adjust the strptime format if the input format varies
                                parsed_date = datetime.strptime(value, "%m/%d/%Y").date()
                                defaults[model_field] = parsed_date.strftime("%Y-%m-%d")
                            except ValueError as e:
                                logger.error(f"Failed to parse date for field '{api_field}' with value '{value}'. Error: {e}")
                                # Optionally, set a default value or continue with an error
                                continue  # Or handle it in a way that suits your needs
                        else:
                            defaults[model_field] = value
                    else:
                        logger.warning(f"Field '{api_field}' is missing in the API results.")
                        continue
                nhtsa_recall, created = await database_sync_to_async(
                    NhtsaRecall.objects.update_or_create)(
                        vin=vin,
                        make=make,
                        model=model,
                        model_year=model_year,
                        defaults=defaults,
                    )
                
                nhtsa_recall_list.append(nhtsa_recall)
                created_list.append(created)

    except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
        logger.error(
            f"Failed to fetch extended vin info for {vin}. Error: {e}")
        return None, None, None, None
    except Exception as e:
        logger.error(
        f"ailed to fetch extended vin info  for {vin}. Error: {e}")
        return None, None, None, None
    logger.info(f"Total records : {len(created_list)}")
    return  nhtsa_recall_list, created_list, count, message    

   