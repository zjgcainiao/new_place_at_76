

from .base import serializers
from apis.models import NhtsaApiCallHistory


# assume this model will make all kinds of api calls to NHTSA and store the results. 
# If the vin is available, it will be associated with the vin record.
class NhtsaApiCallHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NhtsaApiCallHistory
        fields = '__all__'  # or list the specific fields you want
        depth = 2   