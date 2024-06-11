from django.db import models
import re
from datetime import datetime
from django.utils import timezone
from django.db import models
from core_operations.constants import US_COUNTRY_CODE, NUMBER_OF_DAYS_IN_A_YEAR
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, \
    CURRENT_TIME_SHOW_PRECISE_TIME_WITH_TIMEZONE, CURRENT_TIME_WITH_OUT_TIMEZONE

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from model_utils import FieldTracker
