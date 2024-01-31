from .base import serializers
from homepageapp.models import PhoneDescModel

class PhoneDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneDescModel
        fields = '__all__'  # or list the specific fields you want