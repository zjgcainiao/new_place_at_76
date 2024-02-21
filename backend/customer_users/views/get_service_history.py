from .base import render, CustomerUser, login_required

@login_required(login_url='customer_users:customer_user_login')
def get_service_history(request, vehicle_id):
    # Logic to fetch and display service history for a specific vehicle
    return render(request, 'customer_users/service_history.html')