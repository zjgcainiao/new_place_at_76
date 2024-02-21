

from .base import render, CustomerUser
from firebase_admin import auth

def customer_user_register_firebaseauth(request):
    # if request.POST:
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     display_name = request.POST.get('display_name') 
    #     phone_number = request.POST.get('phone_number')
    #     user = auth.create_user(
    #         email=email,
    #         email_verified=False,
    #         phone_number=phone_number,
    #         password=password,
    #         display_name=display_name,
    #         # photo_url = '',
    #         disabled=False
    #     )

    return render(request, 'customer_users/11_customer_user_register_with_firebaseauth.html')