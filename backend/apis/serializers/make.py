from .base import serializers
from homepageapp.models import MakesNewSQL02Model

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakesNewSQL02Model
        fields = '__all__'