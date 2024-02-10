from .base import serializers, timezone
from  django.db import models
from decimal import Decimal, ROUND_HALF_EVEN
class AutomanSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Loop through all datetime fields
        for field in instance._meta.get_fields():
          # Handle datetime fields
            if isinstance(field, models.DateTimeField):
                field_value = getattr(instance, field.name)
                if field_value is not None and timezone.is_naive(field_value):
                    field_value = timezone.make_aware(field_value)
                representation[field.name] = field_value.isoformat() if field_value else None

            # Handle decimal fields
            elif isinstance(field, models.DecimalField):
                field_value = getattr(instance, field.name)
                if field_value is not None:
                    try:
                        # Round to 2 decimal places
                        rounded_value = field_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
                        representation[field.name] = rounded_value
                    except Exception as e:
                        # Handle any exceptions that might occur during rounding
                        representation[field.name] = str(e)

        return representation