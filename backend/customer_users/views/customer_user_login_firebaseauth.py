
from .base import render
from django.conf import settings
from firebase_admin import auth

from .base import logger

def customer_user_login_firebaseauth(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        display_name = request.POST.get('display_name') 
        phone_number = request.POST.get('phone_number')
        user = auth.get_user_by_email(email)
        uid=user.uid
        custom_token = auth.create_custom_token(uid)
        if user:
            print(f"User created successfully with email: {user.email} and phone number: {user.phone_number}. user_uid {user.uid}")
    return render(request, 'customer_users/13_customer_user_login_with_firebaseauth.html')