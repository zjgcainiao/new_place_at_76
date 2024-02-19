from .base import models, POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES, VinNhtsaApiSnapshots,Q


# Define a synchronous function to get the QuerySet of VinNhtsaApiSnapshots (vin_data).
# the function is created to be used in async fetch_latest_vin_data_func()
def get_vin_snapshot_queryset(vin, 
                              variable_ids_list=POPULAR_NHTSA_VARIABLE_IDS, 
                              group_names_list=POPULAR_NHTSA_GROUP_NAMES):
    return VinNhtsaApiSnapshots.objects.filter(
        vin=vin,
        version__in=[4, 5],
        #    Q(version=4) | Q(version=5),
        variable__variable_id__in=variable_ids_list,
        variable__variable_group_name__in=group_names_list,
    ).select_related('variable').order_by( 'vin', 'variable','-created_at')
