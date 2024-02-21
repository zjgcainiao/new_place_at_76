from django.http import JsonResponse
from .base import login_required

@login_required(login_url='customer_users:customer_user_login')
def get_my_vehicles(request):
    # implement your logic here to get vehicle info
    data = {'vehicles': ['Car 1', 'Car 2', 'Car 3']}
    return JsonResponse(data)