import logging
import aiohttp
import asyncio
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, FormView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, LineItemsNewSQL02Model, TextMessagesModel, VinNhtsaApiSnapshots
from apis.serializers import CustomerSerializer, RepairOrderSerializer
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets
import json
from apis.serializers import LineItemsSerializer, TextMessagesSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from internal_users.models import InternalUser
from internal_users.internal_user_auth_backend import InternalUserBackend
from apis.serializers import AddressSerializer, PhoneSerializer, EmailSerializer, CustomerSerializer, RepairOrderSerializer, PaymentSerializer
from apis.api_vendor_urls import NHTSA_API_URL
from core_operations.common_functions import clean_string_in_dictionary_object
from dashboard.async_functions import decrement_version_for_vin_async, update_or_create_vin_snapshots_async, database_sync_to_async
from decouple import config, UndefinedValueError, Csv
from homepageapp.models import LicensePlateSnapShotsPlate2Vin
from homepageapp.models import VinNhtsaApiSnapshots
from django.db import models
# from asgiref.sync import sync_to_async
from apis.api_vendor_urls import PLATE2VIN_API_URL


class RepairOrderViewSet(viewsets.ModelViewSet):
    serializer_class = RepairOrderSerializer

    def get_queryset(self):
        qs = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        qs = qs.prefetch_related('repair_order_customer',
                                 'repair_order_customer__addresses',
                                 'repair_order_customer__addresses',
                                 'repair_order_customer__phones',
                                 'repair_order_customer__emails',
                                 'repair_order_customer__taxes',
                                 'payment_repairorders',
                                 'repair_order_customer__payment_customers'
                                 )
        return qs


class LineItemsViewSet(viewsets.ModelViewSet):

    serializer_class = LineItemsSerializer

    def get_queryset(self):
        return LineItemsNewSQL02Model.objects.prefetch_related(
            'lineitems__lineitem_noteitem',
            'lineitems__lineitem_laboritem',
            'lineitems__parts_lineitems')

# get the most recent 10 text messages


class TextMessagesViewSet(viewsets.ModelViewSet):

    serializer_class = TextMessagesSerializer

    def get_queryset(self):
        return TextMessagesModel.objects.filter(text_customer=self.kwargs['customer_id']).order_by('-text_message_id')[:10]


@api_view(['GET'])
def get_active_customers_api(request):
    # try:
    customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(customers, 20)
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse({'customers': serializer.data})
    # return Response(serialized_customers.data)

    # formatted_data = {
    #     'data': serializer.data
    # }
    # return Response(formatted_data)

    # except PageNotAnInteger:
    #     return Response({'error': 'Invalid page number.'}, status=status.HTTP_400_BAD_REQUEST)
    # except EmptyPage:
    #     return Response({'error': 'Page out of range.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_active_repairorders_api(request):
    if request.method == 'GET':
        # repairorders = RepairOrdersNewSQL02Model.objects.all()
        repairorders = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        repairorders = repairorders.select_related('repair_order_customer'
                                                   ).prefetch_related('repair_order_customer__addresses',
                                                                      'repair_order_customer__addresses',
                                                                      'repair_order_customer__phones',
                                                                      'repair_order_customer__emails',
                                                                      'repair_order_customer__taxes'
                                                                      )
        repairorders = repairorders.prefetch_related('payment_repairorders',
                                                     'repair_order_customer__payment_customers')
        serializer = RepairOrderSerializer(
            repairorders, context={'request': request}, many=True)

        return JsonResponse({'repairorders': serializer.data})

#     elif request.method == 'POST':
#         serializer = RepairOrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', 'DELETE'])
# def repairorders_detail(request, pk):
#     try:
#         student = Student.objects.get(pk=pk)
#     except Student.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = RepairOrderSerializer(student, data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         student.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# 2023-08-04 this is the Login API that was created to respond to react app dashboard_react
# dashboard_react is designed to


@csrf_exempt
@require_POST
def api_internal_user_login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')

    user = InternalUserBackend().authenticate(
        request, email=email, password=password)

    if user is not None:
        login(request, user,
              backend='internal_users.internal_user_auth_backend.InternalUserBackend')

        return JsonResponse({
            'email': user.email,
            # 'user': user,
            # user.groups.filter(name='Technicians').exists(),
            'is_technician': False,  # True,
            'is_authenticated_user': user.is_authenticated,
            'is_internal_user': isinstance(user, InternalUser),
        })
    else:
        # Unauthorized sattus code.
        return JsonResponse({'error': 'Invalid login details.'}, status=401)


async def fetch_single_vin_from_nhtsa_api(vin, vehicle_year):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json&modelyear={vehicle_year}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# return and save result for one vin
# return three variables.


async def fetch_and_save_single_vin_from_nhtsa_api(vin, year):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json&modelyear={year}"
    # url_extended = https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}format=json&modelyear={year}
    logger = logging.getLogger('external_api')
    logger.info(
        f'Initiating an api request to NHTSA.DOT.GOV:{ NHTSA_API_URL}.')
    print(f'Initiating an api request to NHTSA.DOT.GOV:{ NHTSA_API_URL}.')
    # print(url)
    vin_data_list = []
    number_of_downgraded_records = 0
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        # if no data, return an warning in the log
        if data is None:
            logger.warning(
                f"No data returned for VIN {vin} and model year {year}. Skipping further processing.")
            print(
                f"No data returned for VIN {vin} and model year {year}. Skipping further processing.")
            return

        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip(
        ) or None

        results = data.get("Results")

        if results:
            logger.info(
                f'pulling result for vin {vin} and model year {year} was successful.')
            print(
                f'pulling result for vin {vin} and model year {year} was successful.')

            updated_records = await decrement_version_for_vin_async(vin)
            number_of_downgraded_records = updated_records
            if updated_records:
                logger.info(
                    f'decrementing the version number for existing records with the same vin and variable_id before pulling the latest data...')

            for item in results:
                item = clean_string_in_dictionary_object(item)

                # Check the value of Value
                value = item.get("Value", None)
                # Ensure that value_id is a number, otherwise default to None
                try:
                    value_id = int(item.get("ValueId") or 0)
                    if value_id == 0:
                        value_id = None
                except ValueError:
                    value_id = None

                try:
                    # Converts None or '' to 0
                    variable_id = int(item.get("VariableId") or 0)
                    if variable_id == 0:
                        variable_id = None
                except ValueError:
                    variable_id = None

                # Check the value of Variable
                variable_name = item.get("Variable", None)
                if variable_name:
                    variable_name = variable_name.strip() or None

                organized_data = {
                    'results_count': count,
                    'results_message': message,
                    'results_search_criteria': search_criteria,
                    "variable_id": variable_id,
                    "variable_name": variable_name,
                    "value": value,
                    "value_id": value_id,
                    "vin": vin,
                    "source": NHTSA_API_URL,
                    "version": 5  # Reset version to 5 for new data
                }
                vin_data, created = await update_or_create_vin_snapshots_async(vin=vin, variable_id=variable_id, data=organized_data)
                vin_data_list.append(vin_data)

        logger.info(
            f'Vin data has been saved for {vin} and model year {year}. Created?:{created}.')
        if created:
            print(f'saving new vin data? {created}?')
        else:
            print('no new vin data saved.')

        print('func completed.')
        # return the data, the number of records downgraded, and if new records are created in the VinNhtsaSnapshots
        return vin_data_list, number_of_downgraded_records, created

    except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
        logger.error(
            f"Failed to fetch VIN data for {vin} and model year {year}. Error: {e}")
        return None, None, None
    except Exception as e:
        logger.error(
            f"Failed to process and save VIN data for {vin} and model year {year}. Error: {e}")
        return None, None, None

# async function that fetchs a result for a single combo of license plate and state. Vendor: plate2vin


async def fetch_single_plate_data_via_plate2vin_api(license_plate, state, api_url=PLATE2VIN_API_URL):
    logger = logging.getLogger('external_api')
    url = api_url.strip()
    payload = {
        "state": state,
        "plate": license_plate
    }
    logger.info('perform async single plate search using plate2vin api...')
    logger.info('attempting to read any api key stored in the .env...')
    try:
        plate2vin_api_key = config("PLATE2VIN_API_KEY")
    except UndefinedValueError:
        logger.error(
            'Error: The required environment variable PLATE2VIN_API_KEY is not set.')
        raise ValueError(
            "The required environment variable PLATE2VIN_API_KEY is not set.")

    headers = {
        'Authorization': plate2vin_api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()

            success = data.get('success')
            vin_data = data.get('vin', {})
            if success:
                vin_data = clean_string_in_dictionary_object(vin_data)

                # first need to check if there are any existing records with the same license plate and state. this model deos not check the unique on vin field.
                # whenever there is a new
                exists = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(license_plate=license_plate, state=state).exists)()
                if exists:
                    await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(
                        license_plate=license_plate, state=state
                    ).update)(version=models.F('version') - 1)
                # update or create
                plate_data, created = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.update_or_create)(
                    license_plate=license_plate,
                    state=state,
                    defaults={
                        'vin': vin_data.get('vin'),
                        'api_url': api_url,
                        'api_response': data,
                        'year': vin_data.get('year'),
                        'make': vin_data.get('make'),
                        'model': vin_data.get('model'),
                        'trim': vin_data.get('trim'),
                        'name': vin_data.get('name'),
                        'engine': vin_data.get('engine'),
                        'style': vin_data.get('style'),
                        'transmission': vin_data.get('transmission'),
                        'drive_type': vin_data.get('driveType'),
                        'fuel': vin_data.get('fuel'),
                        'color_name': vin_data.get('color', {}).get('name'),
                        'color_abbreviation': vin_data.get('color', {}).get('abbreviation'),
                        'version': 5,
                    }
                )
            return plate_data, success
