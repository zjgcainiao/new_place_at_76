from .base import viewsets,api_view, JsonResponse
from homepageapp.models import CustomersNewSQL02Model
from apis.serializers import CustomerSerializer


@api_view(['GET'])
def get_active_customers_api(request):
    # try:
    customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(customers, 20)
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse({'customers': serializer.data})
    # return Response(serialized_customers.data)

    # formatted_data = {
    #     'data': serializer.data
    # }
    # return Response(formatted_data)

    # except PageNotAnInteger:
    #     return Response({'error': 'Invalid page number.'}, status=status.HTTP_400_BAD_REQUEST)
    # except EmptyPage:
    #     return Response({'error': 'Page out of range.'}, status=status.HTTP_400_BAD_REQUEST)

