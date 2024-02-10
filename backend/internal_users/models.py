# 2023-04-01 created this internal_user model to manage internal employees, contractors and etc.
# chatGPT 4.0 generated.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from talent_management.models import TalentsModel
# from usermanagers import UserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email.strip():
            raise ValueError('A valid email address is required.')
        # hash the password
        # hashed_password = make_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        if password is None or not password.strip():
            raise TypeError('Superusers must have a non-empty password.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_is_admin', True)
        user = self.create_user(email, password=password, **extra_fields)

        return user


class InternalUser(AbstractBaseUser, PermissionsMixin):
    USER_LEVEL_0 = 0
    USER_LEVEL_1 = 1
    USER_LEVEL_2 = 2
    USER_LEVEL_3 = 3
    USER_LEVEL_4 = 4
    USER_LEVEL_5 = 5
    USER_LEVEL_15 = 15
    USER_PERMISSION_LEVELS = (
        (USER_LEVEL_1, 'access level 1'),
        (USER_LEVEL_2, 'access level 2'),
        (USER_LEVEL_3, 'access level 3'),
        (USER_LEVEL_4, 'Level 4 - not used'),
        (USER_LEVEL_5, 'Level 5 - not used.'),
        (USER_LEVEL_15, 'Level 5.5 - not used.'),
    )
    # AUTH_GROUP LIST
    AUTH_GROUP_LEVEL_0 = 0
    AUTH_GROUP_LEVEL_1 = 1
    AUTH_GROUP_LEVEL_2 = 2
    AUTH_GROUP_LEVEL_3 = 3
    AUTH_GROUP_LEVEL_4 = 4
    AUTH_GROUP_LEVEL_5 = 5
    AUTH_GROUP_LEVEL_6 = 6
    AUTH_GROUP_LEVEL_7 = 7
    AUTH_GROUP_LEVEL_8 = 8
    AUTH_GROUP_LEVEL_9 = 9
    AUTH_GROUP_LEVEL_11 = 11
    AUTH_GROUP_LEVEL_12 = 12
    AUTH_GROUP_LEVEL_13 = 13
    AUTH_GROUP_LEVEL_21 = 21
    AUTH_GROUP_LEVEL_88 = 88

    USER_AUTH_GROUP = (
        (AUTH_GROUP_LEVEL_0, 'visitor: ready-only'),
        (AUTH_GROUP_LEVEL_1, 'customer-group'),
        (AUTH_GROUP_LEVEL_2, 'service-technican-group'),
        (AUTH_GROUP_LEVEL_3, 'talent-management-group'),
        (AUTH_GROUP_LEVEL_4, 'accounting-group'),
        (AUTH_GROUP_LEVEL_5, 'manager-group'),
        (AUTH_GROUP_LEVEL_6, 'boardmember-group'),
        # information strucuture group starts with "1x"
        (AUTH_GROUP_LEVEL_11, 'external-developer-group'),
        (AUTH_GROUP_LEVEL_12, 'developer-group'),
        (AUTH_GROUP_LEVEL_13, 'user-management-group'),

        (AUTH_GROUP_LEVEL_21, 'service-technican-group'),
        (AUTH_GROUP_LEVEL_88, 'master-shi-fu-group'),
    )
    id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(_('first name'), max_length=50,blank=False, null=False)
    user_middle_name = models.CharField(
        _('middle name'), max_length=50, null=True)
    user_last_name = models.CharField(_('last name'), max_length=50)
    # to allow user to enter the full name in one field 
    user_name_alternative = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name='email address', unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)

    # 2023-05-31 An existing conflict that talent_created_by_user is linked a user profile (InternalUser model); it is
    # impossible to link a internal_user back to TalentsModel
    # however, the model uses the following three fields to find the correct talent profile.
    # hence we skip the database foreign key linkage. I believe this provides additional isolation to protect employee information
    # that resides in the TalentsModel
    user_talent = models.ForeignKey(
        TalentsModel, on_delete=models.SET_NULL, null=True)
    # user_talent_id = models.IntegerField(null=True)
    user_talent_profile_linkage_is_confirmed = models.BooleanField(
        default=False)
    user_talent_profile_last_linked_date = models.DateTimeField(
        null=True, blank=True)

    user_start_date = models.DateTimeField(null=True)
    user_discharge_date = models.DateTimeField(null=True, blank=True)

    user_is_active = models.BooleanField(_('active'), default=True,
                    help_text=_('Designates whether this user should be treated as active. if the value is False; it means the account has been deactivated.'))
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

        return self.get_user_full_name
    # 2024-02-09: added the following methods to support the user authentication middleware. 
    # The middleware will add one field "user_type" in the request.user.
    def is_internaluser(self):
        return True
    
    def is_customeruser(self):
        return False
    
    @property
    def get_user_full_name(self):
        first_name = self.user_first_name.capitalize(
        ) if self.user_first_name else None
        middle_name = self.user_middle_name.capitalize(
        ) if self.user_middle_name else None
        last_name = self.user_last_name.capitalize() if self.user_last_name else None
        name_fields = [first_name, middle_name, last_name]
        full_name = ' '.join(
            [field for field in name_fields if field is not None])
        return full_name.strip() if full_name.strip() else "User's full name is not available."
    


    class Meta:
        db_table = 'internalusers_new_03'
        ordering = ['-id']
        verbose_name = 'internaluser'
        verbose_name_plural = 'internalusers'
