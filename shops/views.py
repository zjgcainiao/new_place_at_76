from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from dashboard.forms import LicensePlateSearchForm, VINSearchForm
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api
from django.db import models
from asgiref.sync import sync_to_async
from dashboard.async_functions import fetch_latest_vin_data_from_snapshots, database_sync_to_async
import stripe
import logging
import json
from django.http import JsonResponse

logger = logging.getLogger('django')

# renders the vehicle search page for all site viisters (not log in required)


def vehicle_search_product(request):
    vehicle = None

    return render(request, 'shops/10_vehicle_search_product.html')

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
            except Exception as e:
                form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

    return json.dumps(plate_data)


async def search_by_vin(request):
    vin_data_list = []
    # count = 0
    logger = logging.getLogger('django')
    if request.method == 'POST':
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


async def search_by_vin_or_plate(request):
    vin_form = VINSearchForm(prefix="vin")
    plate_form = LicensePlateSearchForm(prefix="plate")
    if request.method == 'POST':
        if 'vin_search' in request.POST:
            vin_form = VINSearchForm(request.POST, prefix="vin")
            # plate_form = LicensePlateSearchForm()  # empty form

            if vin_form.is_valid():
                # process the data in vin_form.cleaned_data
                vin = vin_form.cleaned_data['vin']
                year = vin_form.cleaned_data['year']
                logger.info(
                    f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')
                if not year or not year.strip():
                    year = None

                latest_vin_data = await fetch_latest_vin_data_from_snapshots(vin)

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

        elif 'plate_search' in request.POST:
            plate_form = LicensePlateSearchForm(request.POST, prefix="plate")
            # vin_form = VINSearchForm()  # empty form

            if plate_form.is_valid():
                license_plate = plate_form.cleaned_data['license_plate']
                state = plate_form.cleaned_data['state'].upper()

                try:
                    plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                    if not success:
                        plate_form.add_error(
                            None, 'Failed to fetch VIN for the given License Plate.')
                except Exception as e:
                    plate_form.add_error(
                        None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')
                return redirect('success_url')  # redirect to a new URL

    else:
        vin_form = VINSearchForm()
        plate_form = LicensePlateSearchForm()

    return render(request, 'search_template.html', {'vin_form': vin_form, 'plate_form': plate_form})
