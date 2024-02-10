from .base import csrf_exempt, require_http_methods, JsonResponse
from django.conf import settings
import requests

@csrf_exempt  # Disable CSRF token for this view
@require_http_methods(["POST"])  # Only allow POST requests to this endpoint
def openai_proxy(request):
    # Extract the data from the incoming POST request
    data = request.POST or request.data
    headers = {
        'Authorization': f'Bearer {settings.OPENAI_API_KEY2}',
        'Content-Type': 'application/json',
    }

    try:
        # Forward the request to OpenAI API
        response = requests.post(
            'https://api.openai.com/v1/engines/davinci-codex/completions',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        # Return the response from OpenAI API
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request to OpenAI API
        return JsonResponse({'error': str(e)}, status=502)  # Proxy Error