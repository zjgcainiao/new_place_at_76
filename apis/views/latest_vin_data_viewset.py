from .base import viewsets, IsAuthenticated, IsInternalUser, Response, status
from apis.serializers import LastestVinDataSerializer
from homepageapp.models import VinNhtsaApiSnapshots
from django.core.exceptions import ObjectDoesNotExist

class LastestVinDataViewSet(viewsets.ModelViewSet):
    serializer_class = LastestVinDataSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]

    def get_queryset(self):
        # Your queryset logic here...
        return VinNhtsaApiSnapshots.objects.all().select_related('variable')


    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({"Error": "VIN not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)