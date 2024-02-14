from rest_framework import viewsets
from homepageapp.models import CannedJobLineItemSequence
from apis.serializers import CannedJobLineItemSequenceSerializer

class CannedJobLineItemSequenceViewSet(viewsets.ModelViewSet):
    queryset = CannedJobLineItemSequence.objects.all()
    serializer_class = CannedJobLineItemSequenceSerializer