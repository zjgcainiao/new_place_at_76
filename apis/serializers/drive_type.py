from .base import serializers
from homepageapp.models import DrivesModel
class DriveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivesModel
        fields = '__all__'