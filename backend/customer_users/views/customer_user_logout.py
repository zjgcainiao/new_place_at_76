from .base import redirect, logout, messages

def customer_user_logout(request):
    messages.info(request,
                  f"Hi {request.user.cust_user_email}, you have been signed out.")
    logout(request)
    return redirect('homepageapp:homepage')

