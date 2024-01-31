from .base import serializers

from homepageapp.models import BodyStylesModel

class BodyStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyStylesModel
        fields = '__all__'