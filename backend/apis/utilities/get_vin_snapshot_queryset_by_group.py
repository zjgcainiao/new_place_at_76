from django.db.models import Case, When, Value, IntegerField
from .base import models, POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES, VinNhtsaApiSnapshots, Q
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS_BY_SORTED_GROUPS, POPULAR_NHTSA_VARIABLE_NAMES_BY_SORTED_GROUPS
from apis.serializers import VinNhtsaApiSnapshotsSerializer
from django.http import JsonResponse


def get_vin_snapshot_queryset_by_group(vin,
                                       variable_ids_by_sorted_groups=POPULAR_NHTSA_VARIABLE_IDS_BY_SORTED_GROUPS,
                                       group_names_list=POPULAR_NHTSA_GROUP_NAMES):
    # grouped_querysets = []
    serialized_data = []
    for group_idx, variable_ids_group in enumerate(variable_ids_by_sorted_groups):
        # Define the custom order for the current group
        ordering = [When(variable_id=variable_id, then=Value(idx))
                    for idx, variable_id in enumerate(variable_ids_group)]

        # Query for the current group
        queryset = VinNhtsaApiSnapshots.objects.filter(
            vin=vin,
            variable__variable_id__in=variable_ids_group,
            variable__variable_group_name__in=group_names_list
        ).exclude(
            value__in=[None, '']
        ).select_related('variable').annotate(
            custom_order=Case(*ordering, output_field=IntegerField())
        ).order_by('custom_order', '-created_at')

        # grouped_querysets.append(list(queryset))
        # Serialize the queryset for the current group
        serializer = VinNhtsaApiSnapshotsSerializer(queryset, many=True)
        serialized_data.append(serializer.data)

    # Return serialized data as JsonResponse
    return JsonResponse(serialized_data, safe=False, status=200)
    # Now you have a list of lists of querysets, each sublist corresponding to a group
    # return grouped_querysets
