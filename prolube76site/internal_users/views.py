
# 2023-04-01. ChatGPT 4.0 generated.
# -----------------

from django.conf import settings
from django.shortcuts import render
import googlemaps
from forms import AddressForm

def validate_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = f"{form.cleaned_data['address_line_1']} {form.cleaned_data['address_line_2']}".strip()
            city = form.cleaned_data['city'].strip()
            state = form.cleaned_data['state'].strip()
            zip_code = form.cleaned_data['zip_code'].strip()

            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_result = gmaps.geocode(f"{address}, {city}, {state} {zip_code}")
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return render(request, 'users/address_validated.html', {'location': location})
            else:
                return render(request, 'users/address_not_found.html')
    else:
        form = AddressForm()

    return render(request, 'users/validate_address.html', {'form': form})
