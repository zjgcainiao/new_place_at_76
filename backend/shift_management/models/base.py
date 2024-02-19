from datetime import timedelta
from django.db import models
from internal_users.models import InternalUser
from talent_management.models import TalentsModel
from django.core.exceptions import ValidationError
from internal_users.models import InternalUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import logging

logger = logging.getLogger('django.db')

STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('working', 'Working'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]
