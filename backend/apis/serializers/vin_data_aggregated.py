
from pyexpat import model
from django.shortcuts import get_object_or_404
from apis.serializers import nhtsa_vehicle_id
from .base import serializers
from homepageapp.models import VinNhtsaApiSnapshots, LicensePlateSnapShotsPlate2Vin, RepairOrdersNewSQL02Model, \
    NhtsaDecodedVin
from homepageapp.models import NhtsaSafetyRating, NhtsaDecodedVin, NhtsaVehicleId, NhtsaRecall
from .plate_and_vin_data import PlateAndVinDataSerializer

from .repair_order import RepairOrderSerializer
from .nhtsa_recall import NhtsaRecallSerializer
from .nhtsa_safety_rating import NhtsaSafetyRatingSerializer
from .nhtsa_decoded_vin import NhtsaDecodedVinSerializer
from .vin_nhtsa_snapshot import VinNhtsaApiSnapshotsSerializer
from apis.utilities import database_sync_to_async,fetch_and_save_nhtsa_decoded_vin,fetch_and_save_nhtsa_recalls,fetch_and_save_nhtsa_safety_rating,fetch_and_save_nhtsa_vehicle_id
from asgiref.sync import async_to_sync
class VinDataAggregatedSerializer(serializers.Serializer):

    vin = serializers.CharField(read_only=True)
    # Assume other fields you want to aggregate, initialized as SerializerMethodField
    safety_ratings = serializers.SerializerMethodField()
    recall_info = serializers.SerializerMethodField()
    repair_history = serializers.SerializerMethodField()
    nhtsa_decoded_vin_info = serializers.SerializerMethodField()
    vin_nhtsa_snapshot_info = serializers.SerializerMethodField()

    def get_safety_ratings(self, obj):
        # Logic to fetch safety ratings based on VIN
        vin = obj['vin']
        async_to_sync(fetch_and_save_nhtsa_decoded_vin)(vin)
        ratings = NhtsaSafetyRating.objects.filter(vin=vin)
        return NhtsaSafetyRatingSerializer(ratings, many=True).data

    def get_recall_info(self, obj):
        vin = obj['vin']
        # Logic to fetch recall information based on VIN
        nhtsa_decoded_vin = get_object_or_404(NhtsaRecall, vin=vin)
        make=nhtsa_decoded_vin.make
        model=nhtsa_decoded_vin.model
        model_year=nhtsa_decoded_vin.model_year
        recalls = NhtsaRecall.objects.filter(
            vin=vin,
            make=make,
            model=model,
            model_year=model_year,
            )
        return NhtsaRecallSerializer(recalls, many=True).data
        

    def get_repair_history(self, obj):
        vin = obj['vin']
        repair_orders = RepairOrdersNewSQL02Model.objects.filter(repair_order_vehicle__VIN_number=vin)

        repair_history_data = RepairOrderSerializer(repair_orders, many=True).data
        return repair_history_data


    def get_nhtsa_decoded_vin_info(self, obj):
        vin = obj['vin']
        decoded_vin = NhtsaDecodedVin.objects.filter(vin=vin)
        nhtsa_decoded_vin = NhtsaDecodedVinSerializer(decoded_vin, many=True).data
        return nhtsa_decoded_vin

    def get_vin_nhtsa_snapshot_info(self, obj):
        vin = obj['vin']
        vin_nhtsa_snapshot = VinNhtsaApiSnapshots.objects.filter(vin=vin)
        vin_nhtsa_snapshot_data = VinNhtsaApiSnapshotsSerializer(vin_nhtsa_snapshot, many=True).data
        return vin_nhtsa_snapshot_data
    
    def get_plate_info(self, obj):
        vin = obj['vin']
        plate_info = LicensePlateSnapShotsPlate2Vin.objects.filter(vin=vin)
        plate_info_data = PlateAndVinDataSerializer(plate_info, many=True).data
        return plate_info_data