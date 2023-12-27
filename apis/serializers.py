from rest_framework import serializers
from homepageapp.models import CustomersNewSQL02Model, RepairOrdersNewSQL02Model, LineItemsNewSQL02Model, TextMessagesModel
from homepageapp.models import AddressesNewSQL02Model, PhonesNewSQL02Model, EmailsNewSQL02Model, CustomersNewSQL02Model, PhoneDescModel, PaymentsModel
from homepageapp.models import VinNhtsaApiSnapshots, LicensePlateSnapShotsPlate2Vin
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


class LineItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItemsNewSQL02Model
        fields = '__all__'


class TextMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessagesModel
        fields = '__all__'


class RepairOrderSerializer(serializers.ModelSerializer):
    repair_order_created_at = serializers.DateTimeField()

    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        # representation is a data dictionary. "data" is often used as well.
        representation = super().to_representation(instance)
        repair_order_created_at = instance.repair_order_created_at

        # Check if the datetime is naive before making it aware
        if repair_order_created_at is not None:
            if timezone.is_naive(repair_order_created_at):
                repair_order_created_at = timezone.make_aware(
                    repair_order_created_at)
            representation['repair_order_created_at'] = repair_order_created_at.isoformat()
        return representation

    def validate(self, attrs):
        # You can add custom validation here
        return super().validate(attrs)
    # 2023-12-20 https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    def create(self, validated_data):
        # Custom logic for creation
        return RepairOrdersNewSQL02Model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Custom logic for updating
        instance.field = validated_data.get('field', instance.field)
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    # customer_dob = serializers.DateTimeField()
    customer_created_at = serializers.DateTimeField()
    customer_updated_at = serializers.DateTimeField()

    class Meta:
        model = CustomersNewSQL02Model
        fields = ["__all__"]
        depth = 2

    def get_full_name(self, instance):
        return f"{instance.cust_first_name} {instance.cust_last_name}"

    # The to_representation method is used to transform the data into a format that will be used in the serialized output. In this case, it is taking the customer_created_at date and transforming it into an ISO fo

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_created_at = instance.customer_created_at

        # Check if the datetime is naive before making it aware
        if customer_created_at is not None:
            if timezone.is_naive(customer_created_at):
                customer_created_at = timezone.make_aware(
                    customer_created_at)
            representation['customer_created_at'] = customer_created_at.isoformat()
        return representation


class LastestVinDataSerializer(serializers.ModelSerializer):

    # use to create a nested relationship
    flattened_data = serializers.SerializerMethodField()

    class Meta:
        model = VinNhtsaApiSnapshots
        fields = ['id', 'vin', 'flattened_data', 'variable', 'variable_name', 'value']
        depth = 1

    def get_flattened_data(self, obj):
        # Initialize an empty dictionary to store our flattened data
        flattened_data = {}

        # Access the related NhtsaVariableList object through the foreign key
        variable = obj.variable

        # Check if the variable exists and is not None
        if variable:
            # Use the attributes of the variable object as keys
            # and the corresponding value from VinNhtsaApiSnapshots as the value
            flattened_data[f"{variable.variable_name} (id:{variable.variable_id})"] = obj.value

        # Return the flattened data
        return flattened_data


class PlateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicensePlateSnapShotsPlate2Vin
        fields = ['__all__']
        depth = 1


# added 2023-12-24 
class VinNhtsaApiSnapshotsSerializer(serializers.ModelSerializer):
    """
    Serializer for VinNhtsaApiSnapshots model.
    """
    class Meta:
        model = VinNhtsaApiSnapshots
        fields = ['id', 'vin', 'variable', 'variable_name', 'value', 'value_id']
        depth = 1
# added 2023-12-24 . nested relationship
class PlateAndVinDataSerializer(serializers.ModelSerializer):
    vin_data = serializers.SerializerMethodField()

    class Meta:
        model = LicensePlateSnapShotsPlate2Vin
        fields = ['id', 'api_url', 'license_plate', 'state', 'vin', 
                  'trim','year','make','engine','drive_type','style','fuel',
                  'color_name','color_abbreviation','vin_data',]
        depth = 2

    def get_vin_data(self, obj):
        # Retrieve VinNhtsaApiSnapshots instances related to the VIN
        vin_related_data = VinNhtsaApiSnapshots.objects.filter(vin=obj.vin)
        # Serialize the related data
        return VinNhtsaApiSnapshotsSerializer(vin_related_data, many=True).data