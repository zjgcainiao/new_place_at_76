from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import requests

def validate_final_address(request):
    address = request.GET.get('address')
    # Use the selected API for validation
    response = requests.get('API_ENDPOINT', params={
        'key': settings.GOOGLE_MAPS_API_KEY,
        'input': address,
        'inputtype': 'textquery'
    })
    return JsonResponse(response.json())


