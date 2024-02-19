from .base import serializers
from homepageapp.models import CannedJobsNewSQL02Model

class CannedJobSerializer(serializers.ModelSerializer):

    def get_canned_job_line_items(self, instance):
        return instance.line_items.all().values()
    
    class Meta:
        model = CannedJobsNewSQL02Model
        fields = '__all__'
        depth = 3