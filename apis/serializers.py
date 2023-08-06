from rest_framework import serializers
from homepageapp.models import CustomersNewSQL02Model, RepairOrdersNewSQL02Model, LineItemsNewSQL02Model, TextMessagesModel
from homepageapp.models import AddressesNewSQL02Model, PhonesNewSQL02Model, EmailsNewSQL02Model, CustomersNewSQL02Model, PhoneDescModel, PaymentsModel
from django.utils import timezone


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressesNewSQL02Model
        fields = ['address_line_01', 'address_city',
                  'address_state', 'address_zip_code']


class PhoneDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneDescModel
        fields = '__all__'  # or list the specific fields you want


class PhoneSerializer(serializers.ModelSerializer):
    phone_desc = PhoneDescSerializer(read_only=True)

    class Meta:
        model = PhonesNewSQL02Model
        fields = ['phone_desc', 'phone_number']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailsNewSQL02Model
        fields = ['email_address']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentsModel
        fields = '__all__'  # or list the specific fields you want


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    # payment_customers = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomersNewSQL02Model
        fields = ['customer_first_name', 'customer_last_name',
                  'addresses', 'phones', 'emails',
                  # 'payment_customers',
                  ]


class RepairOrderSerializer(serializers.ModelSerializer):
    repair_order_customer = CustomerSerializer(read_only=True)
    # payment_repairorders = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = ['repair_order_id', 'repair_order_service_status',
                  'repair_order_last_updated_date', 'repair_order_customer',
                  # 'payment_repairorders'
                  ]


class LineItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItemsNewSQL02Model
        fields = '__all__'


class TextMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessagesModel
        fields = '__all__'


# class RepairOrderSerializer(serializers.ModelSerializer):
#         repair_order_created_at = serializers.DateTimeField()
#         class Meta:
#             model = RepairOrdersNewSQL02Model
#             fields = ['repair_order_new_uid_v01',
#                       'repair_order_id',
#                       'repair_order_created_as_estimate',
#                     #   'repair_order_snapshot_order_total_amount',
#                     #   'customer_first_name',
#                     #   'customer_last_name',
#                     #   'customer_middle_name',
#                     # 'customer_dob',
#                     #   'customer_is_deleted',
#                     #   'customer_is_in_social_crm',
#                     #   'customer_is_okay_to_charge',
#                       'repair_order_created_at',
#                      ]
#         def to_representation(self, instance):
#             representation = super().to_representation(instance) # representation is a data dictionary. "data" is often used as well.
#             repair_order_created_at = instance.repair_order_created_at

#             if repair_order_created_at is not None:
#                 representation['repair_order_created_at'] = timezone.make_aware(repair_order_created_at).isoformat()
#             return representation

# class CustomerSerializer(serializers.ModelSerializer):
#     # customer_dob = serializers.DateTimeField()
#     customer_created_at = serializers.DateTimeField()
#     class Meta:
#         model = CustomersNewSQL02Model
#         fields = ['customer_new_uid_v01',

#                   'customer_first_name',
#                   'customer_last_name',
#                   'customer_middle_name',
#                   # 'customer_dob',
#                   'customer_is_deleted',
#                   'customer_is_in_social_crm',
#                   'customer_is_okay_to_charge',
#                    'customer_created_at',
#                   ]

#     def get_full_name(self, instance):
#         return f"{instance.first_name} {instance.last_name}"


#     # The to_representation method is used to transform the data into a format that will be used in the serialized output. In this case, it is taking the customer_created_at date and transforming it into an ISO fo
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         customer_created_at = instance.customer_created_at

#         if customer_created_at is not None:
#             representation['customer_created_at'] = timezone.make_aware(customer_created_at).isoformat()
#         return representation
