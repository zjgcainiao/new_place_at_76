from .base import serializers
from homepageapp.models import CannedJobsNewSQL02Model

class CannedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CannedJobsNewSQL02Model
        fields = '__all__'