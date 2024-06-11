# common imports. sharing with all separate model files (accountclass.py, alert.py, etc)
from django.db import models
from internal_users.models import InternalUser
from core_operations.models import FormattedPhoneNumberField
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import logging
import re
