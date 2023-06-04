import phonenumbers
# from customer_users.forms import AddressForm
from django.shortcuts import render
from django.utils import timezone

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