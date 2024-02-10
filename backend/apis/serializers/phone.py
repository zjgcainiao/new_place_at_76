from .base import serializers
from .phone_desc import PhoneDescSerializer
from homepageapp.models import PhonesNewSQL02Model

class PhoneSerializer(serializers.ModelSerializer):
    phone_desc = PhoneDescSerializer(read_only=True)

    class Meta:
        model = PhonesNewSQL02Model
        fields = ['phone_desc', 'phone_number']
