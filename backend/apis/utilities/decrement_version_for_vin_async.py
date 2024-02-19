
# return the number of records that are affected by udpate() method.

from .base import models, VinNhtsaApiSnapshots
from .database_sync_to_async import database_sync_to_async


# obselete
@database_sync_to_async
def decrement_version_for_vin_async(vin):

    return VinNhtsaApiSnapshots.objects.filter(vin=vin).update(
        version=models.F('version') - 1
    )

