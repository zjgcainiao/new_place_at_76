from rest_framework import serializers
from homepageapp.models import CustomersNewSQL01Model, RepairOrdersNewSQL01Model
from django.utils import timezone

class RepairOrderSerializer(serializers.ModelSerializer):
        repair_order_created_at = serializers.DateTimeField()
        class Meta:
            model = RepairOrdersNewSQL01Model
            fields = ['repair_order_new_uid_v01',
                      'repair_order_id',
                      'repair_order_created_as_estimate',
                    #   'repair_order_snapshot_order_total_amount',
                    #   'customer_first_name',
                    #   'customer_last_name',
                    #   'customer_middle_name',
                    # 'customer_dob',
                    #   'customer_is_deleted',
                    #   'customer_is_in_social_crm',
                    #   'customer_is_okay_to_charge',
                      'repair_order_created_at',
                     ]
        def to_representation(self, instance):
            representation = super().to_representation(instance) # representation is a data dictionary. "data" is often used as well.
            repair_order_created_at = instance.repair_order_created_at

            if repair_order_created_at is not None:
                representation['repair_order_created_at'] = timezone.make_aware(repair_order_created_at).isoformat()
            return representation

class CustomerSerializer(serializers.ModelSerializer):
    # customer_dob = serializers.DateTimeField()
    customer_created_at = serializers.DateTimeField()
    class Meta:
        model = CustomersNewSQL01Model
        fields = ['customer_new_uid_v01',

                  'customer_first_name',
                  'customer_last_name',
                  'customer_middle_name',
                  # 'customer_dob',
                  'customer_is_deleted',
                  'customer_is_in_social_crm',
                  'customer_is_okay_to_charge',
                   'customer_created_at',
                  ]
    
    def get_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_created_at = instance.customer_created_at

        if customer_created_at is not None:
            representation['customer_created_at'] = timezone.make_aware(customer_created_at).isoformat()
        return representation
