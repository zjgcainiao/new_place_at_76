# get the shop's onlne product list from google cloud storage.

from .base import requests, HttpResponse, render, json

def get_online_product_list(request):
    """
    Renders the online product list page.
    """
    try:
        # Fetching the JSON data from the URL
        response = requests.get('https://storage.googleapis.com/vin-doctor.appspot.com/jsons/Stripe/products.json')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        products = data.get('data', [])  # Safely get the 'data' key; returns an empty list if key doesn't exist

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the HTTP request
        print(e)
        # Optionally, log the error here
        return HttpResponse("An error occurred while fetching product data.", status=500)

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(e)
        # Optionally, log the error here
        return HttpResponse("An error occurred while parsing product data.", status=500)

    # Render the template with product data
    return render(request, 'shops/01_get_online_product_list.html', {'products': products})