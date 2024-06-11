
from .base import JsonResponse, database_sync_to_async, fetch_and_save_single_vin_from_nhtsa_api, QuerySet, logger
from apis.utilities import get_vin_snapshot_queryset, fetch_latest_vin_data_func
import json
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


async def fetch_or_save_latest_vin_snapshot_async(request):
    vin = request.GET.get('vin', None)
    if not vin:
        return JsonResponse({'error': 'No VIN provided'}, status=400)
    elif len(vin) < 13:
        return JsonResponse({'error': 'Incomplete VIN provided. At least 13 digits.'}, status=HTTP_400_BAD_REQUEST)

    latest_vin_data_response = await fetch_latest_vin_data_func(vin)
    if not latest_vin_data_response or latest_vin_data_response.status_code != HTTP_200_OK:
        logger.info(
            f'No VIN {vin} found in the database..searching against our vendor APIs..')
        await fetch_and_save_single_vin_from_nhtsa_api(vin)
        # Re-fetch or handle the scenario appropriately
        latest_vin_data_response = await fetch_latest_vin_data_func(vin)

    if not latest_vin_data_response or latest_vin_data_response.status_code != HTTP_200_OK:
        return JsonResponse({'error': 'No vehicle found for this VIN'},
                            status=HTTP_404_NOT_FOUND)

    # Extracting and parsing the JSON content from the JsonResponse
    try:
        latest_vin_data = json.loads(
            latest_vin_data_response.content.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Failed to decode JSON data'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)
    if not latest_vin_data:
        logger.info(
            f'no vin {vin} in the database..searching against our vendor apis..')
        await fetch_and_save_single_vin_from_nhtsa_api(vin)
        # Re-fetch after saving
        latest_vin_data = await fetch_latest_vin_data_func(vin)
    # Convert to list of dictionaries if it's a QuerySet
    if isinstance(latest_vin_data, QuerySet):
        latest_vin_data = await database_sync_to_async(list)(latest_vin_data.values())

    if not latest_vin_data:
        return JsonResponse({'error': 'No vehicle found for this VIN'}, status=HTTP_404_NOT_FOUND)

    # Assuming latest_vin_data is a list of lists of dictionaries
    formatted_content = []
    for entry_list in latest_vin_data:
        if isinstance(entry_list, list):  # Ensure it's a list
            for entry in entry_list:  # Iterate over each dictionary in the list
                if isinstance(entry, dict) and 'flattened_data' in entry:
                    flattened_data = entry['flattened_data']
                else:
                    flattened_data = {}

                formatted_content.append(flattened_data)

    if not formatted_content:
        formatted_content = "No snapshots found for this VIN."
    logger.info(f'the content of the popover is {formatted_content}.')
    # Return the data you want to show in popover
    # return JsonResponse(formatted_content, safe=False)  #
    return JsonResponse({'data': formatted_content})
