from rest_framework.decorators import action
from yaml import serialize
from homepageapp.models import NhtsaRecall
from .base import viewsets, IsAuthenticated, IsInternalUser, Response, status
from apis.serializers import VinDataAggregatedSerializer, NhtsaDecodedVinSerializer, NhtsaSafetyRatingSerializer, \
    NhtsaRecallSerializer, VinNhtsaApiSnapshotsSerializer, RepairOrderSerializer
from homepageapp.models import VinNhtsaApiSnapshots, NhtsaDecodedVin, NhtsaSafetyRating, RepairOrdersNewSQL02Model
from django.core.exceptions import ObjectDoesNotExist
from apis.utilities import database_sync_to_async, fetch_and_save_nhtsa_decoded_vin, fetch_and_save_nhtsa_recalls, fetch_and_save_nhtsa_safety_rating, fetch_and_save_nhtsa_vehicle_id
from asgiref.sync import async_to_sync
from django.db import close_old_connections
from firebase_auth_app.authentication import FirebaseAuthentication


class VinDataAggregatedViewSet(viewsets.ViewSet):
    serializer_class = VinDataAggregatedSerializer
    # permission_classes = [IsAuthenticated, IsInternalUser]
    authentication_classes = [FirebaseAuthentication]

    def list(self, request):
        # return an error response

        return Response({"Error": "Provide a vin number first. Add ?vin=[valid-vin] at the end of the url."}, status=status.HTTP_404_NOT_FOUND)

    # def retrieve(self, request):
    @action(detail=False, methods=['get'], url_path='search_by_vin')
    def search_by_vin(self, request):

        # Logic to fetch data for a specific VIN and prepare the aggregated response
        vin = request.query_params.get('vin', None)
        # vin = request.query_params.get('vin', None)
        # Ensure database connections are properly managed
        close_old_connections()

        async_to_sync(fetch_and_save_nhtsa_decoded_vin)(vin)
        async_to_sync(fetch_and_save_nhtsa_vehicle_id)(vin)
        async_to_sync(fetch_and_save_nhtsa_recalls)(vin)
        async_to_sync(fetch_and_save_nhtsa_safety_rating)(vin)

        safety_ratings = NhtsaSafetyRating.objects.filter(vin=vin).all
        recall_info = NhtsaRecall.objects.filter(vin=vin).all
        repair_orders = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_vehicle__VIN_number=vin).all
        nhtsa_decoded_vin = NhtsaDecodedVin.objects.filter(vin=vin).all
        vin_nhtsa_snapshot = VinNhtsaApiSnapshots.objects.filter(vin=vin), all
        # Fetch recall info, repair history, registration info, etc.
        # Implement similar logic to fetch data for other sections

        # Create a dictionary to represent the aggregated data
        aggregated_data = {
            'vin': vin,
            # 'safety_ratings': NhtsaSafetyRatingSerializer(safety_ratings, many=True).data,
            # 'recall_info': RecallSerializer(recall_info, many=True).data,
            # 'repair_history': RepairOrderSerializer(repair_orders, many=True).data,
            # 'nhtsa_decoded_vin_info': NhtsaDecodedVinSerializer(nhtsa_decoded_vin, many=True).data,
            # 'vin_nhtsa_snapshot_info': VinNhtsaApiSnapshotsSerializer(vin_nhtsa_snapshot, many=True).data,
            # Add data for other sections similarly
        }

        # Serialize the aggregated data
        serializer = VinDataAggregatedSerializer(aggregated_data)
        return Response(serializer.data)

    # def handle_exception(self, exc):
    #     if isinstance(exc, ObjectDoesNotExist):
    #         return Response({"Error": "VIN not found."}, status=status.HTTP_404_NOT_FOUND)
    #     return super().handle_exception(exc)
