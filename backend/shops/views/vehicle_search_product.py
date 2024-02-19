from .base import render, JsonResponse, logging,  model_to_dict, QuerySet, \
    fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api, fetch_latest_vin_data_func

from shops.forms import LicensePlateSearchForm, VINSearchForm
from .manage_vehicle_search_limit import manage_vehicle_search_limit
from  apis.utilities import database_sync_to_async

async def vehicle_search_product(request):
    """
    Performs a vehicle search based on VIN or license plate.
    """
    logger = logging.getLogger('django')
    plate_data={}
    plate_data_id =''
    flattened_data = {}
    max_searches_for_this_view = 1  # Customize this per view or user type
    
    if request.method == 'GET':
        vin_form = VINSearchForm()
        plate_form = LicensePlateSearchForm()
        context = {
            'vin_form': vin_form,
            'plate_form': plate_form,
        }
        return render(request, 'shops/10_vehicle_search_product.html', context)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'action' in request.POST:
        limit_reached, error_context = await database_sync_to_async(manage_vehicle_search_limit)(request, max_searches_for_this_view)
        if limit_reached:
            return JsonResponse(error_context, status=403)
        action_value = request.POST['action'] # action value is used to determine which form is being submitted: vin_form or plate_form
        if action_value == 'action_vin_search':
            vin_form = VINSearchForm(request.POST)
            print(f'user is submitting vin_form....')
            if vin_form.is_valid():
                vin = vin_form.cleaned_data['vin']
                year = vin_form.cleaned_data['year']
                logger.info(
                    f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')
                print(
                    f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')

                if year and year.strip():
                    year = year
                else:
                    year = None

                await fetch_and_save_single_vin_from_nhtsa_api(vin)

                latest_vin_data = await fetch_latest_vin_data_func(vin)

                if isinstance(latest_vin_data, QuerySet):
                    latest_vin_data = await database_sync_to_async(list)(latest_vin_data.values())

                flattened_data['vin'] = vin
                flattened_data = {
                    f"{item['variable_name']} (var_id:{item['variable_id']})": item['value']
                    for item in latest_vin_data
                }

                return JsonResponse(flattened_data, safe=False)

        elif action_value == 'action_plate_search':
            plate_form = LicensePlateSearchForm(request.POST)
            license_plate = ''
            state = ''
            if plate_form.is_valid():
                license_plate = plate_form.cleaned_data['license_plate']
                state = plate_form.cleaned_data['state'].upper(
                ).strip() if plate_form.cleaned_data['state'] else ''

            logger.info(
                f'performing a single plate search for license_plate {license_plate} and state {state}...')
            # print(
            #     f'performing a manual single plate search for license_plate {license_plate} and state {state}...')

            try:
                plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                if not success:
                    plate_form.add_error(
                        None, 'Failed to fetch VIN for the given License Plate.')
                elif plate_data and plate_data.id:
                    flattened_data = await database_sync_to_async(model_to_dict)(plate_data)
            except Exception as e:
                plate_form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

            if plate_data:
                 plate_data_id = plate_data.id

            return JsonResponse({'plate_data_id': plate_data_id})

    if not flattened_data or not plate_data_id or not plate_data_id.strip:
        return JsonResponse({'error': 'No data found'}, status=404)

    return JsonResponse({'plate_data_id': plate_data_id})
