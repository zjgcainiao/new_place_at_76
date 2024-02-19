from uu import decode
from homepageapp.models import NhtsaRecall
from .base import viewsets, IsAuthenticated, IsInternalUser, Response, status
from apis.serializers import VinDataAggregatedSerializer,NhtsaDecodedVinSerializer,NhtsaSafetyRatingSerializer, \
                        Recallerializer,VinNhtsaApiSnapshotsSerializer,RepairOrderSerializer
from homepageapp.models import VinNhtsaApiSnapshots, NhtsaDecodedVin, NhtsaSafetyRating,RepairOrdersNewSQL02Model
from django.core.exceptions import ObjectDoesNotExist
from apis.utilities import database_sync_to_async,fetch_and_save_nhtsa_decoded_vin,fetch_and_save_nhtsa_recalls,fetch_and_save_nhtsa_safety_rating
from asgiref.sync import async_to_sync
from django.db import close_old_connections


class VinDataAggregatedViewSet(viewsets.ViewSet):
    serializer_class = VinDataAggregatedSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def retrieve(self, request, pk=None):
        # Logic to fetch data for a specific VIN and prepare the aggregated response
        vin = pk  # Assuming the VIN is provided in the URL
        
        # Ensure database connections are properly managed
        close_old_connections()    

        # Fetch safety ratings
        recall_info = async_to_sync(fetch_and_save_nhtsa_recalls)(vin)
        safety_ratings = async_to_sync(fetch_and_save_nhtsa_safety_rating)(vin)
        recall_info = NhtsaRecall.objects.filter(vin=vin)
        repair_orders = RepairOrdersNewSQL02Model.objects.filter(repair_order_vehicle__VIN_number=vin)
        nhtsa_decoded_vin = async_to_sync(fetch_and_save_nhtsa_decoded_vin)(vin)
        vin_nhtsa_snapshot = VinNhtsaApiSnapshots.objects.filter(vin=vin)
        # Fetch recall info, repair history, registration info, etc.
        # Implement similar logic to fetch data for other sections
        
        # Create a dictionary to represent the aggregated data
        aggregated_data = {
            'vin': vin,
            'safety_ratings': NhtsaSafetyRatingSerializer(safety_ratings, many=True).data,
            'recall_info': Recallerializer(NhtsaRecall, many=True).data,
            'repair_history': RepairOrderSerializer(repair_orders, many=True).data,
            'nhtsa_decoded_vin_info': NhtsaDecodedVinSerializer(nhtsa_decoded_vin, many=True).data,
            'vin_nhtsa_snapshot_info': VinNhtsaApiSnapshotsSerializer(vin_nhtsa_snapshot, many=True).data,
            # Add data for other sections similarly
        }
        
        # Serialize the aggregated data
        serializer = VinDataAggregatedSerializer(data=aggregated_data)
        return Response(serializer.data)


    # def handle_exception(self, exc):
    #     if isinstance(exc, ObjectDoesNotExist):
    #         return Response({"Error": "VIN not found."}, status=status.HTTP_404_NOT_FOUND)
    #     return super().handle_exception(exc)