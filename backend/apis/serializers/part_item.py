from .base import serializers
from homepageapp.models import PartItemModel

class PartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartItemModel
        fields = '__all__'