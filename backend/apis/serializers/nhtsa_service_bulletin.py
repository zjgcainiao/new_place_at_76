from homepageapp.models import NhtsaServiceBulletin
from .base import serializers

# return service bulletin information based on make, model, year, instead of vin
class NhtsaServiceBulletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaServiceBulletin
        fields = '__all__'  
        depth = 1