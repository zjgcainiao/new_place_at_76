from .base import render, login_required, CustomerUser

@login_required(login_url='customer_users:customer_user_login')
def get_personal_info(request):
    # implement your logic here to get personal info
    if isinstance(request.user, CustomerUser) and request.method == 'GET':
        customer_user = request.user
    return render(request, 'customer_users/30_profile_personal_info.html', {'customer_user': customer_user})
