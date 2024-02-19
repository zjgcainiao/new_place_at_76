from rest_framework import serializers
from homepageapp.models import CannedJobLineItemSequence

class CannedJobLineItemSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CannedJobLineItemSequence
        fields = ['id', 'canned_job', 'line_item', 'sequence']
        depth = 2