from .base import serializers

from homepageapp.models import AddressesNewSQL02Model

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressesNewSQL02Model
        fields = ['address_line_01', 'address_city',
                  'address_state', 'address_zip_code']
