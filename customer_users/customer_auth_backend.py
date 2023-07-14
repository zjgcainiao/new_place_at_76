
from django.contrib.auth.backends import BaseBackend
from customer_users.models import CustomerUser

class CustomerUserBackend(BaseBackend):
    # default authenticate. via phone number
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            # Assume username is the phone number
            customer_user = CustomerUser.objects.get(cust_user_phone_number=phone_number)
        except CustomerUser.DoesNotExist:
            return None

        if customer_user.check_password(password):
            return customer_user

        return None
    #  secondary. via email
    def authenticate_via_email(self, request, email=None, password=None, **kwargs):
        try:
            customer_user = CustomerUser.objects.get(cust_user_email=email)
            if customer_user.check_password(password):
                return customer_user
        except CustomerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomerUser.objects.get(pk=user_id)
        except CustomerUser.DoesNotExist:
            return None
    