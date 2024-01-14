from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from core_operations.forms import AddressForm
import googlemaps
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import json

# def validate_address_manual(request):
#     form = AddressForm()
#     if request.method == 'POST':
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             address = f"{form.cleaned_data['address_line_1']} {form.cleaned_data['address_line_2']}".strip()
#             city = form.cleaned_data['city'].strip()
#             state = form.cleaned_data['state'].strip()
#             zip_code = form.cleaned_data['zip_code'].strip()

#             gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)
#             geocode_result = gmaps.geocode(f"{address}, {city}, {state} {zip_code}")
#             if geocode_result:
#                 location = geocode_result[0]['geometry']['location']
#                 return render(request, 'core_operations/52_address_validated.html', {'location': location})
#             else:
#                 return render(request, 'core_operations/51_address_not_found.html')

#     return render(request, 'core_operations/50_validate_address.html', {'form': form})
def validate_address_manual(request):
    GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY or None
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = f"{form.cleaned_data['address_line_1']} {form.cleaned_data['address_line_2']}".strip()
            city = form.cleaned_data['city'].strip()
            state = form.cleaned_data['state'].strip()
            zip_code = form.cleaned_data['zip_code'].strip()

            gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)
            geocode_results = gmaps.geocode(f"{address}, {city}, {state} {zip_code}")

            if geocode_results:
                # Extract formatted addresses from results
                suggested_addresses = [result['formatted_address'] for result in geocode_results]
                return JsonResponse({'suggestions': suggested_addresses})
        
        return JsonResponse({'suggestions': []})
    

    return render(request, 'core_operations/50_validate_address.html', {'form': form,
                                                                        'GOOGLE_MAP_API_KEY': GOOGLE_MAP_API_KEY})

def validate_address_manual_method2(request):
    address = request.GET.get('addressInput')
    # Use the selected API for validation
    response = requests.get('API_ENDPOINT', params={
        'key': settings.GOOGLE_MAP_API_KEY,
        'input': address,
        'inputtype': 'textquery'
    })
    return JsonResponse(response.json())

def handle_autocomplete_address(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address = data.get('address', '')
        # Process the address as needed
        return JsonResponse({'status': 'success', 'address': address})
    return JsonResponse({'status': 'error'})