from .base import serializers
from homepageapp.models import PaymentsModel

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentsModel
        fields = '__all__'  # or list the specific fields you want