from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from asgiref.sync import sync_to_async
from homepageapp.models import VehiclesNewSQL02Model, LicensePlateSnapShotsPlate2Vin
import logging
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api

logger = logging.getLogger('django.db')
