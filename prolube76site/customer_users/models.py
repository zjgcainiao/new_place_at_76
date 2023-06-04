
# customer_users/models.py
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from homepageapp.models import CustomersNewSQL02Model as Customer

# create the customer user to sign up via phone number. 
# easier for them to sign up and follow up with text messages.

class CustomerUserManager(BaseUserManager):
    use_in_migrations = False
    def create_user(self,  phone_number, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        """
        if  not email and not phone_number:
            raise ValueError('At least one of email or phone number must be provided.')
                # hash the password
        hashed_password = make_password(password)

        email = self.normalize_email(email)
        phone_number = phone_number.strip()
        customer_user = self.model(phone_number=phone_number,
                                   email=email,
                                   **extra_fields)
        # customer_user.set_password(password)
        customer_user.set_password(hashed_password)
        customer_user.save(using=self._db)
        return customer_user

class CustomerUser(AbstractBaseUser):
    # Define additional fields specific to customers
    # For example: personal details, vehicles, service history
    # Make sure to set USERNAME_FIELD to a unique field

    cust_user_id = models.AutoField(primary_key=True)
    cust_user_first_name = models.CharField(_('first name'), max_length=50)
    cust_user_last_name = models.CharField(_('last name'), max_length=50)
    cust_user_phone_number = models.CharField(max_length=20, unique=True,
                                              help_text='enter a valid US phone number.')
    cust_user_country_code = models.CharField(max_length=10, default='+1')
    cust_user_email = models.EmailField(verbose_name='email address', unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    cust_user_start_date = models.DateTimeField(null=True)
    cust_user_discharge_date = models.DateTimeField(null=True, blank=True)
    cust_user_avator_path = models.CharField(max_length=500, blank=False, null=False)
    cust_user_address_01 = models.CharField(max_length=50, blank=False, null=False)
    cust_user_address_02 = models.CharField(max_length=50, blank=False, null=False)
    cust_user_address_city = models.CharField(max_length=50, blank=False, null=False)
    cust_user_address_state = models.CharField(max_length=2, blank=False, null=False)
    cust_user_address_zip = models.CharField(max_length=50, blank=False, null=False)
    cust_user_is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    cust_user_linked_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='users_customers')
    cust_user_linkage_is_confirmed = models.BooleanField(default=False)
    cust_user_last_linked_date = models.DateTimeField(null=True)
    cust_user_created_at = models.DateTimeField(auto_now_add=True)
    cust_user_last_updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'cust_user_phone_number'  # or 'email_address'
    REQUIRED_FIELDS = ['password'] # 'cust_user_phone_number','cust_user_email',

    objects = CustomerUserManager()

    # def __str__(self):
    #     return f'{self.cust_user_first_name} {self.cust_user_last_name}-{self.cust_user_phone_number}'

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
        verbose_name = 'customeruser'
        verbose_name_plural = 'customerusers'

                                                    
