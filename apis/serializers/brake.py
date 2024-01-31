from .base import serializers

from homepageapp.models import BrakesModel

class BrakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrakesModel
        fields = '__all__'