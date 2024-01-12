import io
import requests
import stripe
import logging
import json
from django.urls import reverse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from shops.forms import LicensePlateSearchForm, VINSearchForm
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api
from django.views.decorators.csrf import csrf_exempt
from dashboard.async_functions import database_sync_to_async
from apis.utilities import fetch_latest_vin_data_func
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.views.decorators.http import require_http_methods

# from shops.management.commands.load_stripe_products import Command


if settings.DEBUG:
    # testing mode
    stripe.api_key = settings.STRIPE_SECRET_TEST_KEY
else:
    stripe.api_key = settings.STRIPE_SECRET_TEST_KEY

logger = logging.getLogger('external_api')

def online_product_list(request):
    """
    Renders the online product list page.
    """
    try:
        # Fetching the JSON data from the URL
        response = requests.get('https://storage.googleapis.com/vin-doctor.appspot.com/jsons/Stripe/products.json')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        products = data.get('data', [])  # Safely get the 'data' key; returns an empty list if key doesn't exist

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the HTTP request
        print(e)
        # Optionally, log the error here
        return HttpResponse("An error occurred while fetching product data.", status=500)

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(e)
        # Optionally, log the error here
        return HttpResponse("An error occurred while parsing product data.", status=500)

    # Render the template with product data
    return render(request, 'shops/01_online_product_list.html', {'products': products})

def calculate_order_amount(items):
    """
    Calculates the order amount based on the items.
    """
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = ''
    # settings.STRIPE_WEBHOOK_SECRET 
    endpoint_secret = "we_1OXcwJJQdPkpRk8HDIXvtZel" #"whsec_9fc3fe3c0a22d70e9d62a1b89b6e0abe158aa5c4c8a769b965c78bf422e7219c"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret,
            # settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        #Invlaid Payload

        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
            # Invalid signature
        return HttpResponse(status=400)
    

    # Passed signature verification
    return HttpResponse(status=200)

def create_payment_intent(request, product_id):
    """
    Creates a payment intent for the specified product.
    """
    try:
        # Retrieve the product's price from Stripe
        # Assuming each product has a single price associated with it
        prices = stripe.Price.list(product=product_id, active=True, limit=1)

        if not prices.data:
            return JsonResponse({'error': 'Price not found for the specified product'}, status=404)

        price = prices.data[0].unit_amount  # Price in cents
        intent = stripe.PaymentIntent.create(
            amount=price,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        return JsonResponse(
            {'clientSecret': intent['client_secret']}
        )
    except Exception as e:
        return JsonResponse({'error': f'{e}'}, status=403)

def custom_checkout(request, product_id):
    """
    Renders the custom checkout page for the specified product.
    """

    return render(request, 'shops/21_checkout.html',{
        'product_id': product_id,
    })

def prebuilt_chekcout(request, product_id):
    """
    Renders the prebuilt checkout page for the specified product.
    """
    if settings.DEBUG:
        # testing mode
        YOUR_DOMAIN = 'http://localhost:8000/shops'
    else:
        YOUR_DOMAIN = 'https://www.new76prolubeplus.com/shops'

    prices = stripe.Price.list(product=product_id, active=True, limit=1)
    price_id = prices.data[0].id # Price in cents
    if not prices.data:
        return JsonResponse({'error': 'Price not found for the specified product'}, status=404)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OVk2bJQdPkpRk8HOXVcVfEN', # price_id, # 'price_1OVk2bJQdPkpRk8HOXVcVfEN',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment_success',
            cancel_url=YOUR_DOMAIN + '/payment_cancelled',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

def payment_success(request):
    """
    Renders the payment success page.
    """
    return render(request, 'shops/30_payment_success.html')

def payment_cancelled(request):
    """
    Renders the payment cancelled page.
    """
    return render(request, 'shops/31_payment_cancelled.html')

def stripe_charge(request):
    """
    Handles the Stripe charge request.
    """
    if request.method == 'POST':
        token = request.POST['stripeToken']
        stripe.Charge.create(
            amount=1000,  # amount in cents
            currency='usd',
            description='A description',
            source=token,
        )
        return redirect('some_view_name')

def payment_checkout_react(request):
    """
    Renders the payment checkout page for React app.
    """
    return render(request, 'shops/21_payment_checkout_react.html')

@database_sync_to_async
def set_session_data(request, key, data):
    """
    Sets the session data with the specified key and data.
    """
    request.session[key] = data
    request.session.modified = True  # Ensure the session is saved

async def vehicle_search_product(request):
    """
    Performs a vehicle search based on VIN or license plate.
    """
    logger = logging.getLogger('django')
    plate_data={}
    plate_data_id =''
    flattened_data = {}


    if request.method == 'GET':
        vin_form = VINSearchForm()
        plate_form = LicensePlateSearchForm()
        context = {
            'vin_form': vin_form,
            'plate_form': plate_form,
        }
        return render(request, 'shops/10_vehicle_search_product.html', context)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'action' in request.POST:
        action_value = request.POST['action']

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
            print(
                f'performing a manual single plate search for license_plate {license_plate} and state {state}...')

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

async def export_vin_data_to_pdf(request):
    """
    Exports the VIN data to a PDF file.
    """
    latest_vin_data = database_sync_to_async(request.session.get)(
        'latest_vin_data')

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    y_position = 72

    for entry in latest_vin_data:
        c.drawString(72, y_position, f"{entry['key']}: {entry['value']}")
        y_position += 15

    c.showPage()
    c.save()
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type='application/pdf')
