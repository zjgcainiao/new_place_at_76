import time
import json
import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from django.db import transaction
from django.core.management.base import BaseCommand
from homepageapp.models import Vendors, AddressesNewSQL02Model, VendorAdddresses
from core_operations.utilities import clean_string_in_dictionary_object
from homepageapp.models import NhtsaMake
from apis.utilities import fetch_from_api_url
from apis.api_vendor_urls import NHTSA_GET_ALL_MAKES_URL
from asgiref.sync import sync_to_async


logger = logging.getLogger('management_script')