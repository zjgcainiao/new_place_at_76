from django.urls import reverse
from django.conf import settings
from urllib.parse import urljoin
import aiohttp
from django.http import JsonResponse


async def fetch_vin_aggregated_data(vin):
    # Determine the base URL based on DEBUG setting
    base_url = 'http://127.0.0.1:8000' if settings.DEBUG else 'https://www.new76prolubeplus.com'

    # Dynamically generate the endpoint URL
    endpoint_path = "apis/vin_data_aggregated/search_by_vin/"

    # Construct the full URL
    search_url = urljoin(base_url, endpoint_path) + f"?format=json&vin={vin}"

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            if response.status != 200:
                return JsonResponse({"error": "Failed to retrieve data"}, status=response.status)
            vin_data = await response.json()

    if not vin_data or not isinstance(vin_data, dict):
        return JsonResponse({"error": "No valid data found for the provided VIN"}, status=404)
