from .base import render, CustomerUserRegistrationForm, CustomerUser

def customer_user_registration_success(request):
    if isinstance(request.user, CustomerUser):
        customer_user = request.user
    else:
        customer_user = None
    return render(request, 'customer_users/60_customer_user_registration_success.html', {'customer_user': customer_user})

# only renders the html templates