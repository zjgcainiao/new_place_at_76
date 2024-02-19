
from .base import models, VinNhtsaApiSnapshots
from .database_sync_to_async import database_sync_to_async


@database_sync_to_async
def update_or_create_vin_snapshots_async(vin, variable, data):
    # grab the variable_instance from the lookup table NhtasVariableList model.

    # variable_instance, _ = NhtsaVariableList.objects.get_or_create(
    #     variable_id=variable_id)
    return VinNhtsaApiSnapshots.objects.update_or_create(
        vin=vin,
        variable=variable,
        defaults=data,
    )



