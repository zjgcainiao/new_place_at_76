from .base import viewsets, IsAuthenticated, IsInternalUser,api_view, action, Response, POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_VARIABLE_IDS
from homepageapp.models import VinNhtsaApiSnapshots

from apis.serializers import LastestVinDataSerializer


## this one returns api data based on POPULAR_NHTSA_VARIABLE_IDS
class VinNhtsaApiSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = LastestVinDataSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        # List of variable IDs to filter. imported from core_operations.constants
        variable_ids_list = POPULAR_NHTSA_VARIABLE_IDS
        # vin = self.kwargs.get('vin')
        vin = self.request.query_params.get('vin')
        # print(f'fetched vin number is {vin}')

        if vin:
            qs = VinNhtsaApiSnapshots.objects.filter(
                vin=vin,
                version=5,
                variable__in=variable_ids_list,
            ).order_by('-created_at', 'variable')

            # Sort based on the order of variable_ids_list
            sorted_qs = sorted(
                qs, key=lambda x: variable_ids_list.index(x.variable))
            return sorted_qs
        else:
            return VinNhtsaApiSnapshots.objects.none()