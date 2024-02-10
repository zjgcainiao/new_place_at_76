from .base import serializers
from homepageapp.models import TextMessagesModel


class TextMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessagesModel
        fields = '__all__'
