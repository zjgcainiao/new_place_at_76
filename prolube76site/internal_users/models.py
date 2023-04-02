# 2023-04-01 created this internal_user model to manage internal employees, contractors and etc.
# chatGPT 4.0 generated.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
# from usermanagers import UserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
                # hash the password
        hashed_password = make_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(hashed_password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        # option 1
        # return self.create_user(email, password, **extra_fields)
        # option 2
        # create a user with the hashed password
        user = self.create_user(email, password=password, **extra_fields)
        user.save(using=self._db)
        return user


class InternalUser(AbstractBaseUser, PermissionsMixin):
    USER_PERMISSION_LEVELS = (
            (1, 'Level 1'),
            (2, 'Level 2'),
            (3, 'Level 3'),
        )
    USER_PAY_TYPES = (
        (1, 'Hourly'),
        (2, 'Salary'),
        (3, 'Commission'),
    )
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(_('first name'), max_length=50)
    user_last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(verbose_name= 'email address', unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    date_of_birth = models.DateField(verbose_name='date of birth')
    physical_address_01 = models.CharField(verbose_name='your street address', max_length=100)
    physical_address_02 = models.CharField(max_length=100, blank=True)
    physical_address_city = models.CharField(max_length=50)
    physical_address_state = models.CharField(max_length=2)
    physical_address_zip_code = models.CharField(max_length=10)
    physical_address_country = models.CharField(max_length=50)
    mailing_address_is_the_same_physical_address = models.BooleanField(default=False)
    mailing_address_01 = models.CharField(verbose_name='your street address', max_length=100)
    mailing_address_02 = models.CharField(max_length=100, blank=True)
    mailing_address_city = models.CharField(max_length=50)
    mailing_address_state = models.CharField(max_length=2)
    mailing_address_zip_code = models.CharField(max_length=10)
    mailing_address_country = models.CharField(max_length=50)

    user_permission_level = models.IntegerField(default=0)
    user_pay_type = models.CharField(max_length=50)
    user_hired_date = models.DateField()
    user_discharge_date = models.DateField(null=True, blank=True)
    user_is_active = models.BooleanField(_('active'), default=True, \
                                        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_is_admin = models.BooleanField(default=False)
    user_created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password',]
                    #    'date_of_birth','user_first_name','user_last_name',
                    #    'physical_address_01',
                    #    'physical_address_02',
                    #    'physical_address_city',
                    #    'physical_address_state',
                    #    'physical_address_zip_code',
                    #    'physical_address_country',]

    objects = UserManager()

    def __str__(self):
        return f'{self.user_first_name} {self.user_last_name}'

    class Meta:
        db_table = 'internalusers'
        verbose_name = 'internaluser'
        verbose_name_plural = 'internalusers'



