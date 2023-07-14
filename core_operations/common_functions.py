import phonenumbers
# from customer_users.forms import AddressForm
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
import re
# 
def is_valid_us_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, 'US')
        return phonenumbers.is_valid_number(parsed_number) or phonenumbers.is_possible_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False


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
from homepageapp.models import MakesNewSQL02Model
from django.http import JsonResponse
def get_latest_vehicle_make_list():
# Get a distinct list of makes
    # Get a distinct list of makes
    # makes = MakesNewSQL02Model.objects.values_list('make_name', flat=True)
    
    # makes = MakesNewSQL02Model.objects.exclude(make_name__isnull=True).exclude(make_name__exact='').values_list('make_name', flat=True)
    
    makes = MakesNewSQL02Model.objects.exclude(make_name__isnull=True).exclude(make_name__exact='').all().order_by('make_name')
    make_dict_list = list(makes.values('make_id', 'make_name'))
    make_tuple_list = [(make.pk, make.make_name) for make in makes]
    
    # Create a list of tuples for the choices, removing duplicates using set() and sort the result
    # models = ModelsNewSQL02Model.objects.filter(make_id=make_id)
    return make_tuple_list

# common function 07
from homepageapp.models import ModelsNewSQL02Model
def get_latest_vehicle_model_list():
    models = ModelsNewSQL02Model.objects.exclude(model_name__isnull=True).exclude(model_name__exact='').all().order_by('model_name')
    model_dict_list = list(models.values('model_id', 'model_name'))
    model_tuple_list = [(model.pk, model.model_name) for model in models]
    return model_tuple_list
    # return JsonResponse(model_dict_list, safe=False)


# common function 08
from core_operations.models import US_COUNTRY_CODE
def format_phone_number_to_shop_standard(phone_number):
    phone_number_digits = re.sub(r'\D','', phone_number)
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