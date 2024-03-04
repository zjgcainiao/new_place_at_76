import logging
import aiohttp
import asyncio
from datetime import timedelta
from django.utils.timezone import now
from django.db import close_old_connections, DatabaseError, IntegrityError
from decouple import config, UndefinedValueError, Csv
from core_operations.utilities import clean_string_in_dictionary_object
from homepageapp.models import LicensePlateSnapShotsPlate2Vin, VinNhtsaApiSnapshots, NhtsaVariableList
from apis.api_vendor_urls import PLATE2VIN_API_URL, NHTSA_API_URL
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES
from asgiref.sync import sync_to_async
# from channels.db import database_sync_to_async
from aiohttp import ClientSession
from django.shortcuts import get_object_or_404
from django.db import transaction
import json
import logging
from asgiref.sync import async_to_sync
from dateutil import parser
from shops.models import Vin

logger = logging.getLogger('django.db')
