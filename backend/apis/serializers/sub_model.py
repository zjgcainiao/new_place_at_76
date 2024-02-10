from .base import serializers

from homepageapp.models import SubmodelsModel

class SubModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmodelsModel
        fields = '__all__'
