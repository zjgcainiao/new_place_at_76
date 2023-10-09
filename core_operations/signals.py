from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from asgiref.sync import sync_to_async
from homepageapp.models import VehiclesNewSQL02Model
import logging
from apis.views import fetch_and_save_single_vin_from_nhtsa_api

logger = logging.getLogger('external_api')


@receiver(post_save, sender=VehiclesNewSQL02Model)
def fetch_vin_data_on_new_vehicle(sender, instance, created, **kwargs):

    if created:  # Check if it's a newly created instance.
        logging(
            f'new vehicle record {instance.pk} created. trigger vin data fetching signal for vin {instance.VIN_number}.')
        try:
            # Convert our async function to synchronous for the signal.
            sync_to_async(fetch_and_save_single_vin_from_nhtsa_api(
                instance.VIN_number, instance.vehicle_year))()
        except Exception as e:
            # Catch any general exception
            logger.error(
                f"Failed to fetch and save VIN data for {instance.VIN_number}; model year {instance.vehicle_year} . Error: {e}")
