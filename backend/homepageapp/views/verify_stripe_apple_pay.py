from .base import render, HttpResponse, requests
from django.conf import settings
from decouple import config


def verify_stripe_applepay(request):
    cloud_url = ''
    cloud_url = config('STRIPE_APPLE_PAY_VERIFY_URL', default=None)
    if not cloud_url:
        return HttpResponse('STRIPE_APPLE_PAY_VERIFY_URL not set', status=500)

    try:
        response = requests.get(str(cloud_url))  # Convert cloud_url to str
        # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
    except requests.RequestException as e:
        # Handle any exceptions that occur during the HTTP request
        return HttpResponse(str(e), status=500)

    return HttpResponse(response.content, content_type='text/plain')
