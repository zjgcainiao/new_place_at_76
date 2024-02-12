from django.utils.translation import gettext_lazy
from django.db import models
import uuid
from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from homepageapp.models import RepairOrdersNewSQL02Model as RepairOrder
from django.utils import timezone
from core_operations.models import FormattedPhoneNumberField