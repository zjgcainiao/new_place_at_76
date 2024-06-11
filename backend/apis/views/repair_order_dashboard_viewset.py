from .base import viewsets, IsAuthenticated, IsInternalUser, api_view, action, Response
from homepageapp.models import RepairOrdersNewSQL02Model
from apis.serializers import RepairOrderSerializer
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE

# added on 2023-11-06


class WIPDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsInternalUser]
    serializer_class = RepairOrderSerializer

    def get_queryset(self):
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.

        qs = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1,
            repair_order_phase__lte=5
        ).select_related(
            'repair_order_customer', 'repair_order_vehicle',
        ).prefetch_related('repair_order_customer__addresses',
                           'repair_order_customer__phones',
                           'repair_order_customer__emails',
                           'repair_order_customer__taxes',
                           'payment_repairorders',
                           'repair_order_customer__payment_customers',
                           )

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use pagination if it's set up in the settings
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not set or not needed, serialize the queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def current_time(self, request):
        return Response({'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE})
