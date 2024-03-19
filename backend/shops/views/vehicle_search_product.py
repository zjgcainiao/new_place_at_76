import stat
from .base import render, JsonResponse, logging,  model_to_dict, QuerySet, \
    fetch_and_save_single_vin_from_nhtsa_api, \
    fetch_single_plate_data_via_plate2vin_api, fetch_latest_vin_data_func

from shops.forms import LicensePlateSearchForm, VINSearchForm
from .manage_vehicle_search_limit import manage_vehicle_search_limit
from apis.utilities import database_sync_to_async
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_VARIABLE_NAMES, \
    POPULAR_NHTSA_VARIABLE_NAMES_BY_SORTED_GROUPS, POPULAR_NHTSA_VARIABLE_IDS_BY_SORTED_GROUPS, \
    POPULAR_NHTSA_GROUP_NAMES
from apis.serializers import VinNhtsaApiSnapshotsSerializer, AsyncVinNhtsaApiSnapshotsSerializer


async def vehicle_search_product(request):
    """
    Performs a vehicle search based on VIN or license plate.
    """
    logger = logging.getLogger('django')
    plate_data = {}
    plate_data_id = ''
    flattened_data = {}
    search_success = False

    max_searches_for_this_view = 0  # Customize this per view or user type

    if request.method == 'GET':
        vin_form = VINSearchForm()
        plate_form = LicensePlateSearchForm()
        context = {
            'vin_form': vin_form,
            'plate_form': plate_form,
            'POPULAR_NHTSA_VARIABLE_NAMES_BY_SORTED_GROUPS': POPULAR_NHTSA_VARIABLE_NAMES_BY_SORTED_GROUPS,
        }
        return render(request, 'shops/10_vehicle_search_product.html', context)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # action value is used to determine which form is being submitted: vin_form or plate_form
        # 2024-03-13 also used to idenfity the search type for manage_vehicle_search_limit function
        action_value = request.POST.get('action', None)
        if not action_value:
            JsonResponse({'error': 'Invalid form actions'},
                         safe=False,
                         status=status.HTTP_400_BAD_REQUEST
                         )

        if action_value == 'action_vin_search':
            vin_form = VINSearchForm(request.POST)
            if not vin_form.is_valid():
                return JsonResponse({'error': 'Invalid VIN form data.'},
                                    safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)  # Bad Request

            logger.info(f'user is submitting vin_form....')
            if vin_form.is_valid():
                vin = vin_form.cleaned_data['vin']
                year = vin_form.cleaned_data['year']
                logger.info(
                    f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')

                if year and year.strip():
                    year = year
                else:
                    year = None

                await fetch_and_save_single_vin_from_nhtsa_api(vin)

                vin_snapshots_json = await fetch_latest_vin_data_func(vin)

                # if isinstance(latest_vin_data, QuerySet):
                #     latest_vin_data = await database_sync_to_async(list)(latest_vin_data.values())
                # logger.info(f'latest_vin_data fetched: {latest_vin_data}...')
                # flattened_data['vin'] = vin
                # flattened_data = {
                #     f"{item['variable_name']} (var_id:{item['variable_id']})": item['value']
                #     for item in latest_vin_data
                # }

                if vin_snapshots_json:
                    search_success = True
                    limit_reached, error_context = await database_sync_to_async(manage_vehicle_search_limit)(
                        user=request.user,
                        session=request.session,
                        search_type=action_value,
                        search_success=search_success,
                        manual_max_set=max_searches_for_this_view
                    )
                    if limit_reached:
                        return JsonResponse(error_context,
                                            safe=False,
                                            status=status.HTTP_429_TOO_MANY_REQUESTS)

                return vin_snapshots_json

        elif action_value == 'action_plate_search':
            license_plate = ""
            state = ""
            plate_form = LicensePlateSearchForm(request.POST)
            if not plate_form.is_valid():
                plate_form.add_error(
                    None, 'Invalid License Plate form data')
                return JsonResponse({'error': 'Invalid License Plate form data'},
                                    safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)

            if plate_form.is_valid():
                license_plate = plate_form.cleaned_data['license_plate']
                state = plate_form.cleaned_data['state'].upper(
                ).strip() if plate_form.cleaned_data['state'] else ''

            try:
                logger.info(
                    f'performing a single license_plate search for \
                        license_plate {license_plate} and state {state}...')
                plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                logger.info(
                    f'plate_data fetching is successful?: {success}')
                if not success:
                    plate_form.add_error(
                        None, 'Failed to fetch vehicle info for the given License Plate.')
                elif plate_data and plate_data.id:
                    flattened_data = await database_sync_to_async(model_to_dict)(plate_data)
            except Exception as e:
                plate_form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

            if plate_data and success:

                plate_data_id = plate_data.id
                logger.info(f'plate_data_id is : {plate_data_id}...')
                search_success = True
            # applying search limits on plate search
            limit_reached, error_context = await database_sync_to_async(
                manage_vehicle_search_limit)(
                    user=request.user,
                    session=request.session,
                    search_type=action_value,
                    search_success=search_success,
                    manual_max_set=max_searches_for_this_view
            )
            if limit_reached:
                # too many requests
                return JsonResponse(error_context,
                                    safe=False,
                                    status=status.HTTP_429_TOO_MANY_REQUESTS)

            return JsonResponse({'plate_data_id': plate_data_id},
                                safe=False,
                                status=status.HTTP_200_OK)

    if not flattened_data or plate_data_id is None \
            or not isinstance(plate_data_id, str) or not plate_data_id.strip():

        return JsonResponse({'error': 'No data found'},
                            safe=False,
                            status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({'plate_data_id': plate_data_id},
                        safe=False,
                        status=status.HTTP_200_OK)
