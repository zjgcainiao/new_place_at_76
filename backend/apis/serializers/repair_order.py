from .base import serializers, timezone
from homepageapp.models import RepairOrdersNewSQL02Model



class RepairOrderSerializer(serializers.ModelSerializer):
    repair_order_created_at = serializers.DateTimeField()

    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = "__all__"
        depth = 4

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
    # 2023-12-20 
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    def create(self, validated_data):
        # Custom logic for creation
        return RepairOrdersNewSQL02Model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Custom logic for updating
        instance.field = validated_data.get('field', instance.field)
        instance.save()
        return instance

