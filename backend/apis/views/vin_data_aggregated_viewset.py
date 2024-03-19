from rest_framework.decorators import action
from yaml import serialize
from homepageapp.models import NhtsaRecall
from .base import viewsets, IsAuthenticated, IsInternalUser, Response, status, logger
from apis.serializers import VinDataAggregatedSerializer, NhtsaDecodedVinSerializer, NhtsaSafetyRatingSerializer, \
    NhtsaRecallSerializer, VinNhtsaApiSnapshotsSerializer, RepairOrderSerializer
from homepageapp.models import VinNhtsaApiSnapshots, NhtsaDecodedVin, NhtsaSafetyRating, RepairOrdersNewSQL02Model
from django.core.exceptions import ObjectDoesNotExist
from apis.utilities import database_sync_to_async, fetch_and_save_nhtsa_decoded_vin, \
    fetch_and_save_nhtsa_recalls, fetch_and_save_nhtsa_safety_rating, \
    fetch_and_save_nhtsa_vehicle_id, create_or_update_vin_record, trigger_vin_or_license_plate_fetch_tasks
from asgiref.sync import async_to_sync
from django.db import close_old_connections
from firebase_auth_app.authentication import FirebaseAndSimpleJwtAuthentication


class VinDataAggregatedViewSet(viewsets.ViewSet):
    serializer_class = VinDataAggregatedSerializer
    # permission_classes = [IsAuthenticated, IsInternalUser]  # ,
    # permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAndSimpleJwtAuthentication]

    def list(self, request):
        # return an error response
        vin = request.query_params.get('vin', None)
        if not vin:
            return Response({"Error": "Provide a vin number first. Add ?vin=[valid-vin] at the end of the url."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Error": "do not support to display the list() method."}, status=status.HTTP_404_NOT_FOUND)
    # def retrieve(self, request):

    @action(detail=False, methods=['get'], url_path='search_by_vin')
    def search_by_vin(self, request):
        # Logic to fetch data for a specific VIN and prepare the aggregated response
        vin = request.query_params.get('vin', None)
        if not vin:
            return Response({"Error": "Provide a vin number first. Add ?vin=[valid-vin] at the end of the url."}, status=status.HTTP_400_BAD_REQUEST)
        # vin = request.query_params.get('vin', None)
        # Ensure database connections are properly managed
        close_old_connections()
        # async_to_sync(trigger_vin_or_license_plate_fetch_tasks)(vin)
        async_to_sync(create_or_update_vin_record)(vin)
        async_to_sync(fetch_and_save_nhtsa_decoded_vin)(vin)
        async_to_sync(fetch_and_save_nhtsa_vehicle_id)(vin)
        async_to_sync(fetch_and_save_nhtsa_recalls)(vin)
        async_to_sync(fetch_and_save_nhtsa_safety_rating)(vin)

        # safety_ratings = NhtsaSafetyRating.objects.filter(vin=vin).all
        # recall_info = NhtsaRecall.objects.filter(vin=vin).all
        # repair_orders = RepairOrdersNewSQL02Model.objects.filter(
        #     repair_order_vehicle__VIN_number=vin).all
        # nhtsa_decoded_vin = NhtsaDecodedVin.objects.filter(vin=vin).all
        # vin_nhtsa_snapshot = VinNhtsaApiSnapshots.objects.filter(vin=vin).all
        # Fetch recall info, repair history, registration info, etc.
        # Implement similar logic to fetch data for other sections

        # Create a dictionary to represent the aggregated data
        aggregated_data = {
            'vin': vin,
        }

        # Serialize the aggregated data
        serializer = VinDataAggregatedSerializer(aggregated_data)
        logger.info(
            f'data prepared for search_by_vin is successful...returning the serialized data.')
        return Response(serializer.data)

    # def handle_exception(self, exc):
    #     if isinstance(exc, ObjectDoesNotExist):
    #         return Response({"Error": "VIN not found."}, status=status.HTTP_404_NOT_FOUND)
    #     return super().handle_exception(exc)
