from .base import serializers
from homepageapp.models import LicensePlateSnapShotsPlate2Vin, VinNhtsaApiSnapshots
from .vin_nhtsa_snapshot import VinNhtsaApiSnapshotsSerializer

# added 2023-12-24 . nested relationship


class PlateAndVinDataSerializer(serializers.ModelSerializer):
    vin_data = serializers.SerializerMethodField()
    # vin_data_aggregated = serializers.SerializerMethodField()

    class Meta:
        model = LicensePlateSnapShotsPlate2Vin
        fields = ['id', 'license_plate', 'state', 'vin',
                  'trim', 'year', 'make', 'engine', 'drive_type', 'style', 'fuel',
                  'color_name', 'color_abbreviation', 'vin_data',]
        depth = 2

    def get_vin_data(self, obj):
        # Retrieve VinNhtsaApiSnapshots instances related to the VIN
        vin_related_data = VinNhtsaApiSnapshots.objects.filter(vin=obj.vin)
        # Serialize the related data
        return VinNhtsaApiSnapshotsSerializer(vin_related_data, many=True).data

    # def get_vin_data_aggregated(self, obj):  # New method
    #     # Logic to fetch and aggregate VIN data
    #     vin_data = {
    #         'vin': obj.vin,
    #         # Add other data you want to aggregate here
    #     }
    #     # Serialize the aggregated data
    #     return VinDataAggregatedSerializer(vin_data,
    #                                        many=True).data
