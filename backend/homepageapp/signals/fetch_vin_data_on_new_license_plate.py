

from .base import logger, post_save, LicensePlateSnapShotsPlate2Vin, \
    fetch_and_save_single_vin_from_nhtsa_api, receiver
from datetime import datetime
# this signal created 2023-11-03. when a new license plate record was added to LicensePlateSnapShotsPlate2Vin by a click of button, or for any reasons,
# a new vin copy of the new vin associated with the license plate will be added to the NhtsaVinApiSnapshots model.


@receiver(post_save, sender=LicensePlateSnapShotsPlate2Vin)
async def fetch_vin_data_on_new_license_plate(sender, instance, created, **kwargs):
    today = datetime.date.today()
    logger.info(f'fetch_vin_data_on_new_license_plate signal triggered on \
                {today:%Y-%M-%d %H:%M:%S}...')
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
