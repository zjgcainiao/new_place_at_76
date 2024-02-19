from homepageapp.models import NhtsaDecodedVin
from .base import serializers

class NhtsaDecodedVinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaDecodedVin
        fields = '__all__'  # or list the specific fields you want
        depth = 1