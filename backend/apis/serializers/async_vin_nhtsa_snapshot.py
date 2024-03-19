from .base import serializers

from homepageapp.models import VinNhtsaApiSnapshots

# 2024-03-15


class AsyncVinNhtsaApiSnapshotsSerializer(serializers.ModelSerializer):
    """
    Serializer for Async VinNhtsaApiSnapshots model.
    """

    class Meta:
        model = VinNhtsaApiSnapshots
        fields = ['id', 'vin',  'variable', 'variable_name',
                  'value', 'value_id',
                  'source', 'results_count',
                  'created_at', 'updated_at',
                  ]
        depth = 2

    async def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Perform any async modifications to the representation if needed
        return representation
