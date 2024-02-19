from homepageapp.models import NhtsaSafetyRating

from .base import serializers

class NhtsaSafetyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaSafetyRating
        fields = '__all__'  
        depth = 1