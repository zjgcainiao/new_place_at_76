from .base import serializers
from homepageapp.models import TransmissionsModel
from .automan import AutomanSerializer

class TransmissionSerializer(AutomanSerializer):
    class Meta:
        model = TransmissionsModel
        fields = '__all__'