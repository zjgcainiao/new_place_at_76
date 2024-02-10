from .base import serializers
from homepageapp.models import EnginesModel

class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnginesModel
        fields = '__all__'