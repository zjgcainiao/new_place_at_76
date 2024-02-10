# import django model
from django.db import models
from internal_users.models import InternalUser
from core_operations.models import FormattedPhoneNumberField
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator