

from django.shortcuts import render
from flask import request
from django.http import JsonResponse
from firebase_auth_app.models import FirebaseUser
from shops.forms import VINSearchForm, LicensePlateSearchForm
import logging
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from shops.views import manage_vehicle_search_limit
from  apis.utilities import database_sync_to_async
from django.db.models.query import QuerySet
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_latest_vin_data_func, \
                    fetch_single_plate_data_via_plate2vin_api

def get_firebase_user_dash(request):
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
            'user':FirebaseUser,
        }
        return render(request, 'firebase_auth_app/10_firebase_user_dash.html', {'user':FirebaseUser})
        # return render(request, 'shops/10_vehicle_search_product.html', context)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'action' in request.POST:
        limit_reached, error_context = manage_vehicle_search_limit(request, max_searches_for_this_view)
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

                async_to_sync(fetch_and_save_single_vin_from_nhtsa_api)(vin)

                latest_vin_data =  async_to_sync(fetch_latest_vin_data_func)(vin)

                if isinstance(latest_vin_data, QuerySet):
                    latest_vin_data = list(latest_vin_data.values())

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
                plate_data, success =  async_to_sync(fetch_single_plate_data_via_plate2vin_api)(license_plate, state)
                if not success:
                    plate_form.add_error(
                        None, 'Failed to fetch VIN for the given License Plate.')
                elif plate_data and plate_data.id:
                    flattened_data = model_to_dict(plate_data)
            except Exception as e:
                plate_form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

            if plate_data:
                 plate_data_id = plate_data.id

            return JsonResponse({'plate_data_id': plate_data_id})

    if not flattened_data or not plate_data_id or not plate_data_id.strip:
        return JsonResponse({'error': 'No data found'}, status=404)

    return JsonResponse({'plate_data_id': plate_data_id})


