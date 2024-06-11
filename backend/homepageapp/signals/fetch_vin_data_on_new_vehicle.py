from .base import logger, post_save, VehiclesNewSQL02Model, \
    fetch_and_save_single_vin_from_nhtsa_api, receiver


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
