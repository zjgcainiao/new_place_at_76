from .base import serializers
from homepageapp.models import LicensePlateSnapShotsPlate2Vin

class PlateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicensePlateSnapShotsPlate2Vin
        fields = ['id','license_plate', 'state', 'vin', 'trim','year','make','engine','drive_type','style','fuel','color_name','color_abbreviation','vin_data']
        depth = 1
        
