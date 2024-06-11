import logging
import phonenumbers
from django.db import connections
from django.conf import settings
from django.db.utils import OperationalError
# from customer_users.models import CustomerUser
# from internal_users.models import InternalUser
from dateutil import parser
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from datetime import datetime
from faker import Faker
from asgiref.sync import sync_to_async
from core_operations.constants import US_COUNTRY_CODE
from django.http import JsonResponse
# from customer_users.forms import AddressForm
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from decimal import Decimal, InvalidOperation
import re
from django.core.paginator import Paginator
from django.db import transaction
from django.db import models
import barcode
from io import BytesIO
fake = Faker()

logger = logging.getLogger("django.db")
