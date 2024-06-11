from .base import settings, googlemaps, JsonResponse, AddressForm
from rest_framework import status
from django.contrib import messages


def validate_address_manual(request):

    GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY or None
    if not GOOGLE_MAP_API_KEY:
        messages.error(request, 'Google Maps API key is not set.')
        return JsonResponse({'error': "Google Maps API key is not set."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = f"{form.cleaned_data['address_line_1']} {form.cleaned_data['address_line_2']}".strip()
            city = form.cleaned_data['city'].strip()
            state = form.cleaned_data['state'].strip().upper()
            zip_code = form.cleaned_data['zip_code'].strip()

            gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)
            geocode_results = gmaps.geocode(
                f"{address}, {city}, {state} {zip_code}")

            if geocode_results:
                # Extract formatted addresses from results
                suggested_addresses = [result['formatted_address']
                                       for result in geocode_results]
                return JsonResponse({'suggestions': suggested_addresses}, status=status.HTTP_200_OK)

        return JsonResponse({'suggestions': []})
