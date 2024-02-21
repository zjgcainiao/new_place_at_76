from .base import render, login_required, CustomerUser

@login_required(login_url='customer_users:customer_user_login')
def get_vehicle_search_page(request):
    # implement your logic here to get vehicle info
    customer_user = None
    if isinstance(request.user, CustomerUser) and request.method == 'GET':
        customer_user = request.user
    return render(request, 'customer_users/30_profile_search_vin.html', {'customer_user': customer_user})