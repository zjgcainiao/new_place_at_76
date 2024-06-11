from .base import settings, JsonResponse, requests


def validate_address_manual_method2(request):
    address = request.GET.get('addressInput')

    
    # Use the selected API for validation
    response = requests.get('API_ENDPOINT', params={
        'key': settings.GOOGLE_MAP_API_KEY,
        'input': address,
        'inputtype': 'textquery'
    })
    return JsonResponse(response.json())