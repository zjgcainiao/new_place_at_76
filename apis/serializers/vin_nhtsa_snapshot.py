from .base import serializers

from homepageapp.models import VinNhtsaApiSnapshots

# added 2023-12-24 
class VinNhtsaApiSnapshotsSerializer(serializers.ModelSerializer):
    """
    Serializer for VinNhtsaApiSnapshots model.
    """
    class Meta:
        model = VinNhtsaApiSnapshots
        fields = ['id', 'vin', 'variable', 'variable_name', 'value', 'value_id']
        depth = 1