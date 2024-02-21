

from .base import render, CustomerUser, login_required

@login_required(login_url='customer_users:customer_user_login')
def get_personal_info_v2(request):
    # implement your logic here to get personal info
    if isinstance(request.user, CustomerUser) and request.method == 'GET':
        customer_user = request.user
    return render(request, 'customer_users/30_profile_personal_info_v2.html', {'customer_user': customer_user})