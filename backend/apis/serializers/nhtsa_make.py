from .base import serializers
from homepageapp.models import NhtsaMake

class NhtsaMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaMake
        fields = '__all__'  
        depth = 1