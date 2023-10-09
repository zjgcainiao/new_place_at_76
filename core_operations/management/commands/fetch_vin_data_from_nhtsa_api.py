from django.core.management.base import BaseCommand
from homepageapp.models import VehiclesNewSQL02Model, VinNhtsaAPISnapshots
import aiohttp
import asyncio
import logging
import os
from apis.api_vendor_urls import NHTSA_API_URL
from dashboard.async_functions import decrement_version_for_vin_async,
from django.db.models import Q
import time
from asgiref.sync import sync_to_async
from django.db import models
logger = logging.getLogger('external_api')

# Get the base name of the current script
script_name = os.path.basename(__file__)


class Command(BaseCommand):
    help = 'Fetch VIN data from NHTSA API for each vehicle stored in VehiclesNewSQL02Model and save to VINSearchSnapshots.'

    API_RATE_LIMIT = 10

    async def fetch_vin_nhtsa_api(self, vin, year):
        # Modify the URL if needed to include year or any other parameters

        # url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json&modelyear={year}"
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/{vin}?format=json&modelyear={year}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
        except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
            logger.error(
                f"Error fetching data for VIN {vin} with Model Year {year}: {e}")
            return None
    # vehicles_queryset = await sync_to_async(lambda:VehiclesNewSQL02Model.objects.exclude(Q(VIN_number='') | Q(VIN_number=None)).order_by('-vehicle_id'), thread_sensitive=True)()

    async def async_handle(self, *args, **kwargs):
        start_time = time.time()  # Record the start time
        logger.info(
            f"running {script_name}. The script attempts to pull VIN info for each of vehicle record in VehiclesNewSQL02Model.")
        print(
            f"running {script_name}. The script attempts to pull VIN info for each of vehicle record in VehiclesNewSQL02Model.")

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
            f"Total vehicles with non-empty VIN: {vehicle_count}")
        print(
            f"Total vehicles with non-empty VIN: {vehicle_count}")

        # step 03 Convert the filtered QuerySet to a list for further processing
        vehicles = list(vehicles_queryset)

        # vehicles = await sync_to_async(list, thread_sensitive=True)(vehicles_queryset)

        # vehicles = vehicles.all()

        logger.info(
            f'The scirpt has set up API_RATE_LIMIT as {self.API_RATE_LIMIT}')

        print(
            f'The scirpt has set up API_RATE_LIMIT as {self.API_RATE_LIMIT}')
        logger.info('running aysncio loops...processing...')
        print('running aysncio loops...processing...')

        await self.fetch_and_save_data(vehicles)
        # Run the event loop until all VIN data is fetched
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.fetch_and_save_data(vehicles))

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {script_name} completed in {elapsed_time:.2f} seconds.")
        print(
            f"Script {script_name} completed in {elapsed_time:.2f} seconds.")

    def handle(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_handle(*args, **kwargs))

    # api call limit is set for 10
    async def fetch_and_save_data(self, vehicles):
        # Using asyncio.Semaphore to control concurrency
        # Change the limit value as per your API rate limits
        semaphore = asyncio.Semaphore(10)

        # add this new @sync_to_async decorated function to handle Django ORM sync writting and reading issues

        @sync_to_async
        def update_or_create_record(vin, variable_id, data):
            VinNhtsaAPISnapshots.objects.update_or_create(
                vin=vin,
                variable_id=variable_id,
                defaults=data,
            )
        # .filter() returns a queryset. it won't raise an error but an empty QuerySet.
        # .update () method will then be a no-op on an empty Queryset.

        @sync_to_async
        def update_version_for_vin(vin):
            updated_rows = VinNhtsaAPISnapshots.objects.filter(vin=vin).update(
                version=models.F('version') - 1
            )
            return updated_rows > 0

        async def fetch_and_save(vehicle):
            try:
                # For reading from the ORM
                vin = await sync_to_async(lambda: vehicle.VIN_number.strip() if vehicle.VIN_number else None, thread_sensitive=True)()
                vehicle_year = await sync_to_async(getattr, thread_sensitive=True)(vehicle, "vehicle_year")
                vehicle_id = await sync_to_async(getattr, thread_sensitive=True)(vehicle, "vehicle_id")

                if not vin or not vehicle_year or not vehicle_year.strip():
                    logger.warning(
                        f"Vehicle ID {vehicle_id} has missing VIN or model year.")
                    return

                async with semaphore:
                    data = await self.fetch_vin_nhtsa_api(vin, vehicle_year)
                    if data is None:
                        logger.warning(
                            f"No data returned for VIN {vin} and model year {vehicle_year}. Skipping further processing.")
                        print(
                            f"No data returned for VIN {vin} and model year {vehicle_year}. Skipping further processing.")
                        return

                    # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
                    count = data.get("Count", None)
                    message = data.get("Message", "").strip() or None
                    search_criteria = data.get("SearchCriteria", "").strip(
                    ) or None

                    results = data.get("Results")

                    if results:
                        logger.info(
                            f'pulling result for vin {vin} and model year {vehicle_year} was successful. Source:{NHTSA_API_URL}')
                        print(
                            f'pulling result for vin {vin} and model year {vehicle_year} was successful. Source:{NHTSA_API_URL}')
                        for item in results:

                            # Check the value of Value
                            value = item.get("Value", None)

                            # Ensure that value_id is a number, otherwise default to None
                            try:
                                value_id = int(item.get("ValueId") or 0)
                                if value_id == 0:
                                    value_id = None
                            except ValueError:
                                value_id = None

                            # variable_id = int(item["VariableId"])
                            try:
                                # Converts None or '' to 0
                                variable_id = int(item.get("VariableId") or 0)
                                if variable_id == 0:
                                    variable_id = None
                            except ValueError:
                                variable_id = None

                            # Check the value of Variable Name
                            variable_name = item.get("Variable", None)
                            if variable_name:
                                variable_name = variable_name.strip() or None

                            organized_data = {
                                'results_count': count,
                                'results_message': message,
                                'results_search_criteria': search_criteria,
                                "variable_id": variable_id,
                                "variable_name": variable_name,
                                "value": value,
                                "value_id": value_id,
                                "vin": vin,
                                "source": NHTSA_API_URL,
                                "version": 5  # Reset version to 5 for new data
                            }
                            # decrementing the version by minus -1; latest is set to be 5
                            updated_flag = await update_version_for_vin(vin)
                            if updated_flag:
                                logger.info(
                                    f'decrementing the version number for existing records before pulling the latest data...')
                            # this is the newwer version of await update_version_for_vin(vin)
                            # updated_records = await decrement_version_for_vin_async(vin)
                            # if updated_records:
                            #     logger.info(
                            #         f'decrementing the version number for existing records before pulling the latest data...')
                            # For writing to the VINSearchSnapshots ORM in async way
                            await update_or_create_record(vin, variable_id, organized_data)
            except Exception as e:
                logger.error(f'Error processing VIN {vin}:{e}')
        # Use asyncio.gather to run multiple fetches concurrently
        await asyncio.gather(*(fetch_and_save(vehicle) for vehicle in vehicles))
