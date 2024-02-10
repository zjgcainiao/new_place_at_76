
from .base import JsonResponse, database_sync_to_async, fetch_and_save_single_vin_from_nhtsa_api, fetch_latest_vin_data_from_snapshots,QuerySet


async def fetch_or_save_latest_vin_snapshot_async(request):
    vin = request.GET.get('vin', None)
    if not vin:
        return JsonResponse({'error': 'No VIN provided'}, status=400)
    elif len(vin) < 13:
        return JsonResponse({'error': 'Incomplete VIN provided. At least 13 digits.'}, status=400)

    # Fetch the details based on VIN (you can modify this as per your logic)
    latest_vin_data = await fetch_latest_vin_data_from_snapshots(vin)
    if not latest_vin_data:
        print(
            f'no vin {vin} in the database..searching against our vendor apis..')
        await fetch_and_save_single_vin_from_nhtsa_api(vin)

    # Convert to list of dictionaries if it's a QuerySet
    if isinstance(latest_vin_data, QuerySet):
        latest_vin_data = await database_sync_to_async(list)(latest_vin_data.values())

    if not latest_vin_data:
        return JsonResponse({'error': 'No vehicle found for this VIN'}, status=404)

    # Format for presentation
    formatted_content = ""
    for entry in latest_vin_data:
        formatted_content += f"""
        {entry['variable_name']}: {entry['value']}; 
        """
    if not formatted_content:
        formatted_content = "No snapshots found for this VIN."
    print(f'the content of the popover is {formatted_content}.')
    # Return the data you want to show in popover
    # return JsonResponse(formatted_content, safe=False)  #
    return JsonResponse({'data': formatted_content})