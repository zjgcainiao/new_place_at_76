from .base import serializers
from homepageapp.models import VehiclesNewSQL02Model

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclesNewSQL02Model
        fields = '__all__'

