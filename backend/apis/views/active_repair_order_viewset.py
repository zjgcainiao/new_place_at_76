from .base import viewsets, IsAuthenticated, IsInternalUser
from homepageapp.models import RepairOrdersNewSQL02Model
from apis.serializers import RepairOrderSerializer

class ActiveRepairOrderViewSet(viewsets.ModelViewSet):
    serializer_class = RepairOrderSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        qs = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        qs = qs.prefetch_related('repair_order_customer',
                                 'repair_order_customer__addresses',
                                 'repair_order_customer__addresses',
                                 'repair_order_customer__phones',
                                 'repair_order_customer__emails',
                                 'repair_order_customer__taxes',
                                 'payment_repairorders',
                                 'repair_order_customer__payment_customers'
                                 )
        return qs
