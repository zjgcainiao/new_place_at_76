from .base import viewsets, IsAuthenticated, IsInternalUser,api_view, action, Response, status
from apis.serializers import PlateAndVinDataSerializer
from homepageapp.models import LicensePlateSnapShotsPlate2Vin
from django.core.cache import cache


# added on 2023-12-24. this one returns DRF-viewset data from license plate and state. 
# this viewset uses `PlateAndVinDataSerializer` serializer, which has a nested serializer `VinNhtsaApiSnapshotsSerializer`
class PlateAndVinDataViewSet(viewsets.ModelViewSet):
    queryset = LicensePlateSnapShotsPlate2Vin.objects.all()
    serializer_class = PlateAndVinDataSerializer
    # permission_classes = [IsAuthenticated, IsInternalUser]

    def check_rate_limit(self, request):
            client_ip = self.get_client_ip(request)
            cache_key = f"search_count_{client_ip}"
            search_count = cache.get(cache_key, 0)

            if not request.user.is_authenticated and search_count >= 2:
                return False

            # Update the count in the cache
            if not request.user.is_authenticated:
                if search_count == 0:
                    # Set the cache to expire after 24 hours
                    cache.set(cache_key, 1, 86400)  # 86400 seconds = 24 hours
                else:
                    cache.incr(cache_key)
            return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = super().get_queryset()
        vin = self.request.query_params.get('vin', None)
        if vin:
            queryset = queryset.filter(vin=vin)
        return queryset
    
    # def list(self, request, *args, **kwargs):
    #     if not self.check_rate_limit(request):
    #         return Response({"detail": "Daily search limit reached."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    #     return super().list(request, *args, **kwargs)
    # def retrieve(self, request, *args, **kwargs):
    #     if not self.check_rate_limit(request):
    #         return Response({"detail": "Daily search limit reached."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    #     return super().retrieve(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        # Custom logic for creating a new instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Custom logic for updating an existing instance
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Custom logic for deleting an instance
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Add any other methods you need (e.g., partial_update, retrieve, etc.)

    # Optionally override perform_create, perform_update, perform_destroy if needed
