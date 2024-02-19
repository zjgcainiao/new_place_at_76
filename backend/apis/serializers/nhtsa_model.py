from .base import serializers
from homepageapp.models import NhtsaModel

class NhtsaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaModel
        fields = '__all__'  # or list the specific fields you want
        depth = 1