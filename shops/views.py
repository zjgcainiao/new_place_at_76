import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from shops.forms import LicensePlateSearchForm, VINSearchForm
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api
from django.db import models
from asgiref.sync import sync_to_async
from dashboard.async_functions import fetch_latest_vin_data_from_snapshots, database_sync_to_async
from apis.utilities import fetch_latest_vin_data_func
import stripe
import logging
import json
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.views.decorators.http import require_http_methods


logger = logging.getLogger('django')
# renders the vehicle search page for all site viisters (not log in required)


def vehicle_search_product(request):
    flattened_data = None

    vin_form = VINSearchForm()
    plate_form = LicensePlateSearchForm()
    context = {
        'vin_form': vin_form,
        'plate_form': plate_form,
    }
    return render(request, 'shops/10_vehicle_search_product.html', context)


# standard django based checkout page, using ES6 module based stripe.js

def payment_checkout(request):
    return render(request, 'shops/21_payment_checkout.html')

# react app based checkout.


def payment_checkout_react(request):
    return render(request, 'shops/21_payment_checkout_react.html')

# backend stripe charge function


def stripe_charge(request):

    if request.method == 'POST':
        token = request.POST['stripeToken']
        stripe.Charge.create(
            amount=1000,  # amount in cents
            currency='usd',
            description='A description',
            source=token,
        )
        return redirect('some_view_name')


async def search_by_plate(request):

    plate_data = []
    success = False

    if request.method == 'POST':
        form = LicensePlateSearchForm(request.POST or None)
        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            state = form.cleaned_data['state'].upper()

            try:
                plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                if not success:
                    form.add_error(
                        None, 'Failed to fetch information for the given license plate.')
                # Assuming `plate_data` is an instance of `LicensePlateSnapShotsPlate2Vin`:
                plate_data = await database_sync_to_async(model_to_dict)(plate_data)
            except Exception as e:
                form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

    return JsonResponse(plate_data)


async def search_by_vin(request):
    logger = logging.getLogger('django')
    vin_data_list = []
    # count = 0
    logger = logging.getLogger('django')
    if request.method == 'POST' and 'action' in request.POST:
        form = VINSearchForm(request.POST)
        if form.is_valid():
            vin = form.cleaned_data['vin']
            year = form.cleaned_data['year']
            logger.info(
                f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')

            vin_data_list, number_of_downgraded_records, created = await fetch_and_save_single_vin_from_nhtsa_api(vin, year)
    else:
        form = VINSearchForm()

    return json.dumps(vin_data_list)


@database_sync_to_async
def set_session_data(request, key, data):
    request.session[key] = data
    request.session.modified = True  # Ensure the session is saved


# used in shops/search_by_vin_or_plate
# 2023-11-04
async def search_by_vin_or_plate(request):
    flattened_data = None
    if request.method == 'GET':
        vin_form = VINSearchForm()
        plate_form = LicensePlateSearchForm()
        context = {
            'vin_form': vin_form,
            'plate_form': plate_form,
        }
        return render(request, 'shops/10_vehicle_search_product.html', context)

    # AJAX POST request handling
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'action' in request.POST:
        action_value = request.POST['action']
        # defined in forms.py
        if action_value == 'action_vin_search':
            vin_form = VINSearchForm(request.POST)
            print(f'user is submitting vin_form....')
            if vin_form.is_valid():
                # process the data in vin_form.cleaned_data
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

                # Fetch the latest vin from VinNhtsaApiSnapshots model
                await fetch_and_save_single_vin_from_nhtsa_api(vin)

                latest_vin_data = await fetch_latest_vin_data_func(vin)

                # if not latest_vin_data:
                #     print(
                #         f'no vin {vin} in the database..searching against our vendor apis..')
                #     await fetch_and_save_single_vin_from_nhtsa_api(vin)

                # latest_vin_data = await fetch_latest_vin_data_from_snapshots(vin)

                # Convert to list of dictionaries if it's a QuerySet
                if isinstance(latest_vin_data, QuerySet):
                    latest_vin_data = await database_sync_to_async(list)(latest_vin_data.values())

                # save a copy into request.session. aysnc
                # await set_session_data(request, 'latest_vin_data', latest_vin_data)

                flattened_data = {
                    f"{item['variable_name']} (var_id:{item['variable_id']})": item['value']
                    for item in latest_vin_data
                }
                # Assuming 'vin' is the VIN you're interested in
                flattened_data['vin'] = vin
                # print(f'here is the flattened data: {flattened_data}')
                # flattened_data = json.dumps(flattened_data, indent=4)
                # print(f'printing out flattened vin data.222...')
                # print(flattened_data)
                return JsonResponse(flattened_data, safe=False)

        elif action_value == 'action_plate_search':
            plate_form = VINSearchForm(request.POST)
            if plate_form.is_valid():
                license_plate = plate_form.cleaned_data['license_plate']
                state = plate_form.cleaned_data['state'].upper(
                ).strip() if plate_form.cleaned_data['state'] else ''

            logger.info(
                f'performing a manual single plate search for license_plate{ license_plate} and state {state}...')
            print(
                f'performing a manual single plate search for license_plate {license_plate} and state {state}...')

            try:
                plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                if not success:
                    plate_form.add_error(
                        None, 'Failed to fetch VIN for the given License Plate.')
            except Exception as e:
                plate_form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

            # Assuming `plate_data` is an instance of `LicensePlateSnapShotsPlate2Vin`
            flattened_data = await database_sync_to_async(model_to_dict)(plate_data)

            return JsonResponse(flattened_data, safe=False)
        else:
            # If the form is not valid, you can return an error message or empty data.
            return JsonResponse({'error': 'Invalid form data'}, status=400)

    # If no POST or no search
    if not flattened_data:
        return JsonResponse({'error': 'No data'}, status=404)

    return JsonResponse(flattened_data, safe=False)

# 2023-11-13 requring io canvas and HttpResponse


async def export_vin_data_to_pdf(request):

    # Fetch the data from the session or database
    latest_vin_data = request.session.get(
        'latest_vin_data')

    # Create a byte stream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Initialize Y position
    y_position = 72

    # Draw the data into the canvas
    for entry in latest_vin_data:
        c.drawString(72, y_position, f"{entry['key']}: {entry['value']}")
        y_position += 15  # Move down the y position for the next line

    # Finish up the page and save the buffer
    c.showPage()
    c.save()
    buf.seek(0)

    # Return the buffer as a PDF response
    return HttpResponse(buf.getvalue(), content_type='application/pdf')
