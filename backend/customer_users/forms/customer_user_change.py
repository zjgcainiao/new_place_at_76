from typing_extensions import ReadOnly
from .base import CustomerUser, forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm


class CustomerUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomerUser
        fields = ['cust_user_email', 'cust_user_first_name', 'cust_user_last_name', 
                  'cust_user_address_01', 'cust_user_address_02', 'cust_user_address_city',
                  'cust_user_address_state', 'cust_user_address_zip', 'cust_user_phone_number']
        readonly_fields = ['user_start_date', 'user_is_active', 'is_superuser', 'user_is_admin',
                           'cust_user_linkage_is_confirmed', 'cust_user_linked_customer']
