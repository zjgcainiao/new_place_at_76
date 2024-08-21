from .base import csrf_exempt, HttpResponse, stripe, settings, logger
from stripe.error import SignatureVerificationError
from django.http import JsonResponse, HttpResponseBadRequest

@csrf_exempt
def stripe_webhook(request, environment='test'):
    # Check if the environment is either 'live' or 'test'
    if environment not in ['live', 'test']:
        return HttpResponseBadRequest("Invalid environment specified")
    
    # Lowercase the environment for consistency
    environment = environment.lower()

    # Determine the endpoint secret based on the environment and configuration
    
    if settings.DEBUG and not settings.DJANGO_PROD_ENV:
        # Local development environment
        environment = 'test' # Force the environment to be 'test' in local development
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_LOCAL
    elif environment == 'test' and not settings.STRIPE_LIVE_MODE_ON:
        # Staging environment
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_TEST
    elif environment == 'live' and settings.STRIPE_LIVE_MODE_ON:
        # Production environment
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_LIVE
    else:
        # Incorrect environment and settings combination
        return JsonResponse({'error': 'Configuration error: invalid environment and settings combination.'}, status=400)

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret,
        )
    except ValueError:
        # Invalid payload
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except SignatureVerificationError:
        # Invalid signature
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    except Exception as e:
        # Other unexpected errors
        return JsonResponse({'error': str(e)}, status=500)

    # Passed signature verification
    # Response for successful processing
    return JsonResponse({'status': 'success'}, status=200)
