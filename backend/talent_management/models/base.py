from core_operations.constants import US_COUNTRY_CODE, NUMBER_OF_DAYS_IN_A_YEAR, LIST_OF_STATES_IN_US
from core_operations.models import FormattedPhoneNumberField, YearsOfWorkField
from django.db import models
import re
from datetime import date
from datetime import datetime
# from internal_users.models import InternalUser
from django.utils import timezone
from faker import Faker

fake = Faker()
