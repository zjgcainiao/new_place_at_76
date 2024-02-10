from .base import viewsets, IsAuthenticated, IsInternalUser, api_view, JsonResponse
from homepageapp.models import RepairOrdersNewSQL02Model
from apis.serializers import RepairOrderSerializer
## older way to provide active repair orders via GET request


@api_view(['GET'])
def get_active_repairorders_api(request):
    if request.method == 'GET':
        # repairorders = RepairOrdersNewSQL02Model.objects.all()
        repairorders = RepairOrdersNewSQL02Model.objects.filter(
            repair_order_phase__gte=1, repair_order_phase__lte=5)
        repairorders = repairorders.select_related('repair_order_customer'
                                                   ).prefetch_related('repair_order_customer__addresses',
                                                                      'repair_order_customer__addresses',
                                                                      'repair_order_customer__phones',
                                                                      'repair_order_customer__emails',
                                                                      'repair_order_customer__taxes'
                                                                      )
        repairorders = repairorders.prefetch_related('payment_repairorders',
                                                     'repair_order_customer__payment_customers')
        serializer = RepairOrderSerializer(
            repairorders, context={'request': request}, many=True)

        return JsonResponse({'repairorders': serializer.data})
