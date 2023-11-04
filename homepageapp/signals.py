from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from asgiref.sync import sync_to_async
from homepageapp.models import VehiclesNewSQL02Model, LicensePlateSnapShotsPlate2Vin
import logging
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api

logger = logging.getLogger('django.db')


@receiver(post_save, sender=VehiclesNewSQL02Model)
async def fetch_vin_data_on_new_vehicle(sender, instance, created, **kwargs):

    if created:  # Check if it's a newly created instance.
        logger.info(
            f'A new vehicle record {instance.pk} was created. Triggering vin data fetching signal for vin {instance.VIN_number} and model year {instance.vehicle_year}')
        try:
            # Convert our async function to synchronous for the signal.
            await fetch_and_save_single_vin_from_nhtsa_api(
                instance.VIN_number, instance.vehicle_year)
        except Exception as e:
            # Catch any general exception
            logger.error(
                f"Failed to fetch and save VIN data for {instance.VIN_number}; model year {instance.vehicle_year} . Error: {e}")


# this signal created 2023-11-03. when a new license plate record was added to LicensePlateSnapShotsPlate2Vin by a click of button, or for any reasons,
# a new vin copy of the new vin associated with the license plate will be added to the NhtsaVinApiSnapshots model.

@receiver(post_save, sender=LicensePlateSnapShotsPlate2Vin)
async def fetch_vin_data_on_new_vehicle(sender, instance, created, **kwargs):

    if created:  # Check if it's a newly created instance.
        logger.info(
            f'New license plate record added {instance.license_plate} was created. Attempting to fetch data for associated vin {instance.vin} from NHTSA.GOV .')
        try:
            # Convert our async function to synchronous for the signal.
            await fetch_and_save_single_vin_from_nhtsa_api(
                instance.vin, instance.year)
        except Exception as e:
            # Catch any general exception
            logger.error(
                f"Failed to fetch and save VIN data for {instance.vin}. Error: {e}")
