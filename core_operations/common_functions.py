from asgiref.sync import sync_to_async
from core_operations.models import US_COUNTRY_CODE
from homepageapp.models import ModelsNewSQL02Model
from django.http import JsonResponse
from homepageapp.models import MakesNewSQL02Model
import phonenumbers
# from customer_users.forms import AddressForm
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
import re
from datetime import datetime
from faker import Faker
import random
import logging
from django.core.paginator import Paginator
from django.db import transaction
from django.db import models
from homepageapp.models import VinNhtsaAPISnapshots

fake = Faker()

#


def is_valid_us_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, 'US')
        return phonenumbers.is_valid_number(parsed_number) or phonenumbers.is_possible_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False


def make_timezone_aware(input_datetime, datetime_formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%f']):
    """
    Convert a naive datetime string or datetime object to a timezone-aware datetime object.

    Parameters:
    - input_datetime: The naive datetime string or datetime object.
    - datetime_formats: A list of datetime formats to try for parsing. Defaults to include common formats.

    Returns:
    - A timezone-aware datetime object or None.
    """
    if input_datetime is None:
        return None

    if isinstance(input_datetime, datetime):
        native_datetime = input_datetime
    elif isinstance(input_datetime, str):
        native_datetime = None
        for fmt in datetime_formats:
            try:
                native_datetime = datetime.strptime(input_datetime, fmt)
                break
            except ValueError:
                continue
        if native_datetime is None:
            return None
    else:
        raise TypeError(
            "The input must be either a datetime object or a string.")

    return timezone.make_aware(native_datetime)


# def validate_address(request):
#     if request.method == 'POST':
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             address = f"{form.cleaned_data['address_line_1']} {form.cleaned_data['address_line_2']}".strip()
#             city = form.cleaned_data['city'].strip()
#             state = form.cleaned_data['state'].strip()
#             zip_code = form.cleaned_data['zip_code'].strip()

#             gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
#             geocode_result = gmaps.geocode(f"{address}, {city}, {state} {zip_code}")
#             if geocode_result:
#                 location = geocode_result[0]['geometry']['location']
#                 return render(request, 'users/address_validated.html', {'location': location})
#             else:
#                 return render(request, 'users/address_not_found.html')
#     else:
#         form = AddressForm()

#     return render(request, 'users/validate_address.html', {'form': form})


# common function 02
def generate_today_date_format():
    # Get the current timezone setting
    timezone_setting = timezone.get_current_timezone()

    # Get the current date and time in the specified timezone
    current_datetime = timezone.now().astimezone(timezone_setting)

    # Generate the today's date formatted as 'YYYY_MM_DD_'
    today_date = current_datetime.strftime('%Y_%m_%d_')

    # Generate the full datetime formatted as 'YYYY_MM_DD_HH_MMMM'
    today_full_datetime = current_datetime.strftime('%Y_%m_%d_%H_%M')

    return today_date, today_full_datetime


# common function 03
def format_string_with_underscore(string):
    # Replace whitespace and hyphens with underscores
    formatted_string = string.replace(' ', '_').replace('-', '_')

    return formatted_string

# common function 04


def deformat_phone_numbers(phone_number):
    # Remove non-digit characters from the phone number
    deformatted_number = ''.join(filter(str.isdigit, phone_number))

    return deformatted_number


# common function 05
def capitalize_first_letters(string):
    # Split the string into individual words
    words = string.split()

    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]

    # Join the capitalized words back into a single string
    capitalized_string = ' '.join(capitalized_words)

    return capitalized_string


# common function 06
def get_latest_vehicle_make_list():
    # Get a distinct list of makes
    # makes = MakesNewSQL02Model.objects.values_list('make_name', flat=True)

    # makes = MakesNewSQL02Model.objects.exclude(make_name__isnull=True).exclude(make_name__exact='').values_list('make_name', flat=True)

    makes = MakesNewSQL02Model.objects.exclude(make_name__isnull=True).exclude(
        make_name__exact='').all().order_by('make_name')

    make_dict_list = list(makes.values('make_id', 'make_name'))
    make_tuple_list = [(make.pk, make.make_name) for make in makes]

    # Create a list of tuples for the choices, removing duplicates using set() and sort the result
    # models = ModelsNewSQL02Model.objects.filter(make_id=make_id)
    return make_tuple_list


# common function 07


def get_latest_vehicle_model_list():
    models = ModelsNewSQL02Model.objects.exclude(model_name__isnull=True).exclude(
        model_name__exact='').all().order_by('model_name')
    model_dict_list = list(models.values('model_id', 'model_name'))
    model_tuple_list = [(model.pk, model.model_name) for model in models]
    return model_tuple_list
    # return JsonResponse(model_dict_list, safe=False)


# common function 08
def format_phone_number_to_shop_standard(phone_number):
    phone_number_digits = re.sub(r'\D', '', phone_number)
    if len(phone_number_digits) == 10:
        full_phone_number_digits = US_COUNTRY_CODE + phone_number_digits
        # Format the phone number as "+1 (818) 223-4456"
        return '+{}({}){}-{}'.format(
            full_phone_number_digits[0:1],
            full_phone_number_digits[1:4],
            full_phone_number_digits[4:7],
            full_phone_number_digits[7:11],
        )
    else:
        raise ValueError('The input must be a 10-digit US phone number.')


# common function 09
logger = logging.getLogger('django')

# created on 2023-09-27
# this function will iterrate all fields in a model and update any matched fields with the following match pattern.
# default database is referred to as 'demo'. This function intends to be used orginally with "popluate_with_dummy_data.py" management script.
# use 'demo' database as default input.

# common function 10
# this function udpate


def update_model_with_dummy_data(model, databaseName='demo', chunk_size=1000):
    logger.info(f"Updating the model {model} in database {databaseName}...")
    updated_records_count = 0  # Counter for updated records
    # reference to the fake methods but not calling them yet.
    patterns_to_update = {
        r"(_first_name|first_name|FirstName)": fake.first_name,
        r"(_last_name|last_name|LastName)": fake.last_name,
        r"(_middle_name|middle_name|MiddleName)": lambda: "Middle " + datetime.now().strftime('%y%m%d'),
        r"(PhoneNum|phone_number$|Phone$|phone$)": lambda: fake.phone_number().split('x')[0].strip(),
        r"(address_line_01|^address_|Address$)": fake.street_address,
        r"(Email$|email$|^email_address)": fake.email,
        r"(address_city|city)": fake.city,
        r"(zip_code|zipcode)": fake.postcode,
        r"(VIN|vin)": fake.vin,
        r"(License|licence_plate_number|license_plate_nbr)": fake.license_plate,
    }

    # Paginate the queryset
    objects_paginator = Paginator(
        model.objects.using(databaseName).all(), chunk_size)

    for page_num in objects_paginator.page_range:

        with transaction.atomic(databaseName):
            # model.objects.all():
            for obj in objects_paginator.page(page_num).object_list:
                updated = False  # Initialize the updated flag
                for field in obj._meta.fields:

                    for pattern, fake_data_func in patterns_to_update.items():
                        if re.search(pattern, field.name):
                            # Check if it's a CharField or EmailField before updating
                            if isinstance(field, models.CharField) or isinstance(field, models.EmailField):
                                setattr(obj, field.name, fake_data_func())
                                updated = True
                            else:
                                logger.info(
                                    f" {field.name} in {model} is not a CharField. Skipping..")
                                continue

                if updated:
                    obj.save(using=databaseName)
                    updated_records_count += 1
                    # logger.info(
                    #     f"Updated record with ID: {obj.pk} in model {model.__name__}.")

    return updated_records_count


def clean_string_in_dictionary_object(data):
    for key, value in data.items():
        if isinstance(value, str):
            cleaned_value = value.strip()
            data[key] = cleaned_value if cleaned_value else None
    return data
