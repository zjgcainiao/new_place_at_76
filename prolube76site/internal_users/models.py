# 2023-04-01 created this internal_user model to manage internal employees, contractors and etc.
# chatGPT 4.0 generated.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
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
            raise ValueError('The Email field must be set.')
        # hash the password
        # hashed_password = make_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # the hashed_password was unncessary.
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        # option 1
        # return self.create_user(email, password, **extra_fields)
        # option 2
        # create a user with the hashed password
        user = self.create_user(email, password=password, **extra_fields)

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        user.save(using=self._db)
        return user

class InternalUser(AbstractBaseUser, PermissionsMixin):
    USER_LEVEL_1 = 1
    USER_LEVEL_2 = 2
    USER_LEVEL_3 = 3
    USER_PERMISSION_LEVELS = (
            (USER_LEVEL_1, 'Level 1'),
            (USER_LEVEL_2, 'Level 2'),
            (USER_LEVEL_3, 'Level 3'),
        )
    AUTH_GROUP_LEVEL_0 = 0
    AUTH_GROUP_LEVEL_1 = 1
    AUTH_GROUP_LEVEL_2 = 2
    AUTH_GROUP_LEVEL_3 = 3
    AUTH_GROUP_LEVEL_4 = 4
    AUTH_GROUP_LEVEL_5 = 5
    AUTH_GROUP_LEVEL_6 = 6
    AUTH_GROUP_LEVEL_7 = 7
    AUTH_GROUP_LEVEL_88 = 88

    USER_AUTH_GROUP = (
        (AUTH_GROUP_LEVEL_0, 'visitor: ready-only'),
        (AUTH_GROUP_LEVEL_0, 'customer-group'),
        (AUTH_GROUP_LEVEL_2, 'internal-user-group'),
        (AUTH_GROUP_LEVEL_3, 'talent-management-group'),
        (AUTH_GROUP_LEVEL_4, 'accounting-group'),
        (AUTH_GROUP_LEVEL_5, 'it-group'),
        (AUTH_GROUP_LEVEL_6, 'manager-group'),
        (AUTH_GROUP_LEVEL_7, 'boardmember-group'),
        (AUTH_GROUP_LEVEL_88, 'master-shi-fu-group'),
        )
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(_('first name'), max_length=50)
    user_last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(verbose_name='email address', unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)

    # 2023-05-31 An existing conflict that talent_created_by_user is linked a user profile (InternalUser model); it is
    # impossible to link a internal_user back to TalentsModel
    # however, the model uses the following three fields to find the correct talent profile.
    # hence we skip the database foreign key linkage. I believe this provides additional isolation to protect employee information
    # that resides in the TalentsModel

    user_talent_id = models.IntegerField(null=True)
    user_talent_profile_linkage_is_confirmed = models.BooleanField(default=False)
    user_talent_profile_last_linked_date =  models.DateTimeField(null=True, blank=True)

    user_start_date = models.DateTimeField(null=True)
    user_discharge_date = models.DateTimeField(null=True, blank=True)

    user_is_active = models.BooleanField(_('active'), default=True, 
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_is_admin = models.BooleanField(default=False)
    user_auth_group = models.PositiveSmallIntegerField(choices=USER_AUTH_GROUP,
                                                       default=AUTH_GROUP_LEVEL_0,
                                                       )
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_last_updated_at = models.DateTimeField(auto_now=True)

    # define the username for this internal_user module is email.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password',]

    objects = UserManager()

    def __str__(self):
        return f'{self.user_first_name} {self.user_last_name}'

    class Meta:
        db_table = 'internalusers_new_03'
        verbose_name = 'internaluser'
        verbose_name_plural = 'internalusers'



