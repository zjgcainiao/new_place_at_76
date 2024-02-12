from django.db import models
from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
