from .base import viewsets, IsAuthenticated, IsInternalUser,api_view, action, \
      Response, POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES, ObjectDoesNotExist,status
from homepageapp.models import VinNhtsaApiSnapshots
from django.db.models import Case, When, Value, IntegerField
from apis.serializers import VinNhtsaApiSnapshotsSerializer


## this one returns api data based on POPULAR_NHTSA_VARIABLE_IDS
class VinNhtsaSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = VinNhtsaApiSnapshotsSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        # List of variable IDs to filter. imported from core_operations.constants
        variable_ids_list = POPULAR_NHTSA_VARIABLE_IDS
        group_names_list=POPULAR_NHTSA_GROUP_NAMES
        # vin = self.kwargs.get('vin')
        vin = self.request.query_params.get('vin')
        
        if vin:
            # Generate a list of When conditions for each variable_id in the order specified
            # it replaces the sorted() function
            ordering_case = Case(*[When(variable_id=variable_id, then=Value(idx)) for idx, variable_id in enumerate(variable_ids_list)], output_field=IntegerField())
            qs = VinNhtsaApiSnapshots.objects.filter(
                vin=vin,
                version__in=[4,5],
                variable__in=variable_ids_list,
                variable__variable_group_name__in=group_names_list,
            ).select_related('variable'
                ).annotate(
                    custom_order=ordering_case
                    ).order_by('vin', 'variable', 'custom_order', '-created_at')

            # Sort based on the order of variable_ids_list
            # sorted_qs = sorted(
            #     qs, key=lambda x: variable_ids_list.index(x.variable))
            # return sorted_qs
            return qs
        else:
            return VinNhtsaApiSnapshots.objects.none()
    
    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({"Error": "VIN not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)