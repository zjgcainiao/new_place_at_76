from .base import serializers
from homepageapp.models import LaborItemModel

class LaborItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaborItemModel
        fields = '__all__'