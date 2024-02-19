from homepageapp.models import NhtsaRecall
from .base import serializers

class Recallerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaRecall
        fields = '__all__'  
        depth = 1