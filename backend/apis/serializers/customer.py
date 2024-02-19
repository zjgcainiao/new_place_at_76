from .base import serializers, timezone
from .address import AddressSerializer
from .phone import PhoneSerializer
from .email import EmailSerializer
from homepageapp.models import CustomersNewSQL02Model

class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    # payment_customers = PaymentSerializer(many=True, read_only=True)
    
    def get_full_name(self, instance):
        return f"{instance.cust_first_name} {instance.cust_middle_name}{instance.cust_last_name}"

    class Meta:
        model = CustomersNewSQL02Model
        fields = ['customer_first_name', 
                  'customer_last_name','customer_middle_name'
                  'addresses', 'phones', 'emails',
                  # 'payment_customers',
                  ]
        depth = 3
    # The to_representation method is used to transform the data into a format that will be used in the serialized output. 
    # In this case, it is taking the customer_created_at date and transforming it into an ISO formatted string.
    # the benefit of using an ISO formatted string is that it is a standard format that can be easily parsed by other systems.
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_created_at = instance.customer_created_at

        # Check if the datetime is native before making it aware
        if customer_created_at is not None:
            if timezone.is_naive(customer_created_at):
                customer_created_at = timezone.make_aware(
                    customer_created_at)
            representation['customer_created_at'] = customer_created_at.isoformat()
        return representation