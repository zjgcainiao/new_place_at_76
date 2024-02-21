from homepageapp.models import NhtsaRecall
from .base import serializers

class NhtsaRecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaRecall
        fields = '__all__'  
        depth = 1