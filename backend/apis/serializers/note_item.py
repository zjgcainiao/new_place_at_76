from .base import serializers
from homepageapp.models import NoteItemsNewSQL02Model

class NoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteItemsNewSQL02Model
        fields = '__all__'