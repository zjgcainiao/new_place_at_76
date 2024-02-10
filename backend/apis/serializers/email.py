from .base import serializers
from homepageapp.models import EmailsNewSQL02Model

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailsNewSQL02Model
        fields = ['email_address']
