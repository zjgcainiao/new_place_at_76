from .base import JsonResponse
from homepageapp.models import CustomersNewSQL02Model

def search_customer_by_phone(request):
    phone_number = request.GET.get('phone_number_entered', None)
    customers = CustomersNewSQL02Model.objects.filter(
        phones__phone_number_digits_only__contains=phone_number)

    # Create a list to hold the customer data
    customer_data = []

    for customer in customers:
        # Fetch related phone numbers for each customer
        phone_numbers = [p.phone_number for p in customer.phones.all()]

        # Create a dictionary holding the customer data and their related phone numbers
        data = {
            'customer_id': customer.customer_id,
            'get_customer_full_name': customer.get_customer_full_name,
            'phone_numbers': phone_numbers,
        }

        customer_data.append(data)

    return JsonResponse(customer_data, safe=False)
