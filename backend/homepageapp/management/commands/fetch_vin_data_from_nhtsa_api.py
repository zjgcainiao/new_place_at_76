"""
Management command script to fetch VIN data from the NHTSA API.

This script queries the VehiclesNewSQL02Model for vehicles and fetches
updated VIN data from an external API, storing results in VINSearchSnapshots.

Usage:
    python manage.py fetch_vin_data_from_nhtsa_api.py

Requirements:
    - asgiref, Django


Versions:
    - 2023-10-13 version 1.0

"""

from django.core.management.base import BaseCommand
from homepageapp.models import VehiclesNewSQL02Model, VinNhtsaApiSnapshots
import aiohttp
import asyncio
import logging
import os
from apis.api_vendor_urls import NHTSA_API_URL, PLATE2VIN_API_RATE_LIMIT
from dashboard.async_functions import decrement_version_for_vin_async
from apis.views import fetch_and_save_single_vin_from_nhtsa_api
from django.db.models import Q
import time
from asgiref.sync import sync_to_async
from django.db import models


logger = logging.getLogger('management_script')

# Get the base name of the current script
script_name = os.path.basename(__file__)


class Command(BaseCommand):
    help = 'Fetch VIN data from NHTSA API for each vehicle stored in VehiclesNewSQL02Model and save to VINSearchSnapshots.'
    if PLATE2VIN_API_RATE_LIMIT:
        API_RATE_LIMIT = PLATE2VIN_API_RATE_LIMIT
    else:
        API_RATE_LIMIT = 10

    async def async_handle(self, *args, **kwargs):
        start_time = time.time()  # Record the start time
        logger.info(
            f"running {script_name}. V2023-10-13. The script attempts to pull latest VIN info categoried by variable_ids for each of vehicle record stored in VehiclesNewSQL02Model.")
        # print(
        #     f"running {script_name}. V2023-10-13. The script attempts to pull latest VIN info categoried by variable_ids for each of vehicle record stored in VehiclesNewSQL02Model.")

        # Get the list of vehicles from the Vehicle model
        # step 01 Filter the vehicles
        vehicles_queryset = await sync_to_async(
            lambda: list(VehiclesNewSQL02Model.objects.exclude(
                Q(VIN_number='') | Q(VIN_number=None)).order_by('-vehicle_id')),
            thread_sensitive=True
        )()

        # step 02 Get the count of vehicles
        # vehicle_count = vehicles.count()
        vehicle_count = len(vehicles_queryset)

        # vehicle_count = await sync_to_async(vehicles_queryset.count, thread_sensitive=True)()
        # Log the count
        logger.info(
            f"Total vehicles with non-empty VIN existing: {vehicle_count}")
        # print(
        #     f"Total vehicles with non-empty VIN existing: {vehicle_count}")

        # step 03 Convert the filtered QuerySet to a list for further processing
        vehicles = list(vehicles_queryset)

        logger.info(
            f'The scirpt has set up API_RATE_LIMIT as {self.API_RATE_LIMIT} while fetching data')

        # print(
        #     f'The scirpt has set up API_RATE_LIMIT as {self.API_RATE_LIMIT}')
        logger.info('running aysncio loops...processing...')
        print('running aysncio loops...processing...')

        await self.fetch_and_save_data(vehicles)

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        # print(
        #     f"Script {script_name}  completed. Total running time: {elapsed_time:.2f} seconds.")

    def handle(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_handle(*args, **kwargs))

    # api call limit is set for 10
    async def fetch_and_save_data(self, vehicles):

        semaphore = asyncio.Semaphore(self.API_RATE_LIMIT)

        async def fetch_and_save(vehicle):
            try:
                # For reading from the ORM
                vin = await sync_to_async(lambda: vehicle.VIN_number.strip() if vehicle.VIN_number else None, thread_sensitive=True)()
                vehicle_year = await sync_to_async(getattr, thread_sensitive=True)(vehicle, "vehicle_year")
                vehicle_id = await sync_to_async(getattr, thread_sensitive=True)(vehicle, "vehicle_id")

                if not vin or not vehicle_year or not vehicle_year.strip():
                    logger.warning(
                        f" VIN or model year is missing or incomplete for the existing vehicle record {vehicle_id},")
                    return

                async with semaphore:
                    # data = await self.fetch_vin_nhtsa_api(vin, vehicle_year)
                    vin_data_list, updated_records, created = await fetch_and_save_single_vin_from_nhtsa_api(vin, vehicle_year)

            except Exception as e:
                logger.error(f'Error processing VIN {vin}:{e}')
        # Use asyncio.gather to run multiple fetches concurrently
        await asyncio.gather(*(fetch_and_save(vehicle) for vehicle in vehicles))
