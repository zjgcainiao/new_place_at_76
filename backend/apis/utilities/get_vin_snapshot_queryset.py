from .base import models, POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES, VinNhtsaApiSnapshots, Q
from django.db.models import Case, When, Value, IntegerField
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS_BY_SORTED_GROUPS, POPULAR_NHTSA_VARIABLE_NAMES_BY_SORTED_GROUPS

# Define a synchronous function to get the QuerySet of VinNhtsaApiSnapshots (vin_data).
# the function is created to be used in async fetch_latest_vin_data_func()


def get_vin_snapshot_queryset(vin,
                              variable_ids_list=POPULAR_NHTSA_VARIABLE_IDS,
                              group_names_list=POPULAR_NHTSA_GROUP_NAMES):
    # return VinNhtsaApiSnapshots.objects.filter(
    #     vin=vin,
    #     # version__in=[4, 5],
    #     #    Q(version=4) | Q(version=5),
    #     variable__variable_id__in=variable_ids_list,
    #     variable__variable_group_name__in=group_names_list,
    # ).select_related('variable').order_by('vin', 'variable', '-created_at')

    # Generate a list of When clauses to define the custom order
    ordering = [When(variable_id=variable_id, then=Value(idx))
                for idx, variable_id in enumerate(variable_ids_list)]

    return VinNhtsaApiSnapshots.objects.filter(
        vin=vin,
        variable__variable_id__in=variable_ids_list,
        variable__variable_group_name__in=group_names_list
    ).exclude(
        # Exclude records where value is null or an empty string
        value__in=[None, '']
    ).select_related('variable').annotate(
        custom_order=Case(*ordering, output_field=IntegerField())
    ).order_by('vin', 'variable', 'custom_order', '-created_at')
