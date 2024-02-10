
from django.contrib.auth.backends import BaseBackend
from customer_users.models import CustomerUser


class CustomerUserBackend(BaseBackend):

    def authenticate(self, request, **kwargs):
        phone_number = kwargs.get('phone_number')
        email = kwargs.get('email')
        password = kwargs.get('password')
        
        try:
            if email:
                customer_user = CustomerUser.objects.get(cust_user_email=email)
                
            elif phone_number:
                customer_user = CustomerUser.objects.get(cust_user_phone_number=phone_number)
            else:
                return None

            if customer_user.check_password(password):
                return customer_user
            return None
        except CustomerUser.DoesNotExist:
            return None
        except CustomerUser.MultipleObjectsReturned:
            # Handle this scenario as needed.
            # Maybe log this as this is an unexpected scenario.
            return None


    def get_user(self, user_id):
        try:
            return CustomerUser.objects.get(pk=user_id)
        except CustomerUser.DoesNotExist:
            return None
