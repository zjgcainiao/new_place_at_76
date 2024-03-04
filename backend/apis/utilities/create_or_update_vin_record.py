import asyncio
from asgiref.sync import sync_to_async
from shops.models import Vin
from .base import logger
from django.db import IntegrityError, transaction


async def create_or_update_vin_record(vin, defaults=None):
    """
    Asynchronously creates a new VIN record or updates an existing one.

    Args:
        vin (str): The VIN to check for and potentially create/update.
        defaults (dict, optional): A dictionary of fields and values to use 
                                    for the create or update operation. 
    """
    savepoint = ''
    defaults = {} if defaults is None else defaults
    try:
        # create a savepoint
        savepoint = await sync_to_async(transaction.savepoint)()
        vin_obj, created = await sync_to_async(Vin.objects.get_or_create)(
            vin=vin, defaults=defaults
        )
        if not created:
            for field, value in defaults.items():
                setattr(vin_obj, field, value)
            await sync_to_async(vin_obj.save)()

        # Commit if successful
        await sync_to_async(transaction.savepoint_commit)(savepoint)
        logger.info(f"VIN record {'created' if created else 'updated'}: {vin}")
        return vin_obj, created

    except IntegrityError as e:
        await sync_to_async(transaction.savepoint_rollback)(savepoint)
        logger.error(f"Database integrity error: {e}")
        raise ValueError("Invalid data format in 'defaults'") from e
    except Exception as e:  # Catch potential timeout or other unexpected errors
        await sync_to_async(transaction.savepoint_rollback)(savepoint)
        logger.error(f"Error during VIN operation: {e}")
        raise RuntimeError(
            "VIN record operation failed. Please try again.") from e
