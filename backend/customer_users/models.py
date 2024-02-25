
# customer_users/models.py
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from homepageapp.models import CustomersNewSQL02Model as Customer
from django.core.exceptions import ValidationError
from firebase_auth_app.models import FirebaseUser

# create the customer user to sign up via phone number.
# easier for them to sign up and follow up with text messages.


class CustomerUserManager(BaseUserManager):
    use_in_migrations = False

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(
                'The email field is required.')

        email = self.normalize_email(email)
        # if phone_number is not None:
        #     phone_number = phone_number.strip()
        # else:
        #     phone_number is None
        customer_user = self.model(cust_user_email=email, **extra_fields)
        # customer_user.set_password(password)
        customer_user.set_password(password)
        customer_user.save(using=self._db)
        return customer_user


class CustomerUser(AbstractBaseUser):
    # Define additional fields specific to customers
    # For example: personal details, vehicles, service history
    # Make sure to set USERNAME_FIELD to a unique field

    cust_user_id = models.AutoField(primary_key=True)
    cust_user_first_name = models.CharField(_('first name'), max_length=50)
    cust_user_last_name = models.CharField(
        _('last name'), max_length=50, null=True, blank=True)
    cust_user_middle_name = models.CharField(
        _('middle name'), max_length=50, null=True)
    cust_user_preferred_name = models.CharField(
        _('preferred name'), max_length=50, help_text='The preffered name.', null=True)
    cust_user_phone_number = models.CharField(max_length=20,  # unique=True, still using email as the default
                                              help_text='enter a valid US phone number.', null=True)
    cust_user_country_code = models.CharField(max_length=10, default='+1')
    cust_user_name_alternate = models.CharField(
        max_length=200, blank=True, null=True)
    firebase_uid = models.CharField(
        max_length=50, blank=True, null=True, unique=True, help_text='The firebase user id.')
    cust_user_email = models.EmailField(
        verbose_name='Email', unique=True)
    cust_user_email_verified = models.BooleanField(
        verbose_name='Email Verified?', default=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    cust_user_start_date = models.DateTimeField(null=True)
    cust_user_discharge_date = models.DateTimeField(null=True, blank=True)
    cust_user_avator_path = models.CharField(
        max_length=500, blank=False, null=False)
    cust_user_address_01 = models.CharField(
        max_length=50, blank=False, null=False)
    cust_user_address_02 = models.CharField(
        max_length=50, blank=False, null=False)
    cust_user_address_city = models.CharField(
        max_length=50, blank=False, null=False)
    cust_user_address_state = models.CharField(
        max_length=2, blank=False, null=False)
    cust_user_address_zip = models.CharField(
        max_length=50, blank=False, null=False)
    cust_user_is_active = models.BooleanField(_('active'), default=True,
                                              help_text=_('Indicates the user active status.'))
    cust_user_linked_customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name='users_customers')
    cust_user_linkage_is_confirmed = models.BooleanField(default=False)
    cust_user_last_linked_date = models.DateTimeField(null=True)
    # cust_user_linked_firebaseuser = models.ForeignKey(
    #     FirebaseUser, on_delete=models.SET_NULL, null=True,related_name='cust_user_firebaseuser')
    customer_user_lastest_ip_address = models.GenericIPAddressField(null=True)

    cust_user_created_at = models.DateTimeField(auto_now_add=True)
    cust_user_last_updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'cust_user_email'  # or 'email_address'
    # 'cust_user_phone_number','cust_user_email',
    REQUIRED_FIELDS = ['password']

    objects = CustomerUserManager()
    # added the following methods to support the user authentication middleware. see InternalUser model.

    def __str__(self):
        return f'{self.cust_user_full_name}'

    def is_internaluser(self):
        return False

    def is_customeruser(self):
        return True
    # Full name property field

    @property
    def cust_user_full_name(self):
        first_name = self.cust_user_first_name
        last_name = self.cust_user_last_name
        full_name = ' '.join(filter(None, [first_name, last_name]))
        if full_name:
            full_name = full_name.capitalize()
        return full_name

    # Full address property field
    @property
    def cust_user_full_address(self):
        address_fields = [
            self.cust_user_address_01,
            self.cust_user_address_02,
            self.cust_user_address_city,
            self.cust_user_address_state,
            self.cust_user_address_zip,
        ]
        full_address = ', '.join(filter(None, address_fields))
        return full_address

    class Meta:
        db_table = 'customerusers_new_03'
        ordering = ['-cust_user_id']
        verbose_name = 'customeruser'
        verbose_name_plural = 'customerusers'
