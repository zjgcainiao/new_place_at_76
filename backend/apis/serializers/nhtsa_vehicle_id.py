from .base import serializers
from homepageapp.models import NhtsaVehicleId

class NhtsaVehicleIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaVehicleId
        fields = '__all__'  # or list the specific fields you want
        depth = 1