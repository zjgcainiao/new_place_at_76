from .base import viewsets, IsAuthenticated, IsInternalUser
from apis.serializers import TextMessagesSerializer
from homepageapp.models import TextMessagesModel

class TextMessagesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInternalUser]
    serializer_class = TextMessagesSerializer

    def get_queryset(self):
        return TextMessagesModel.objects.filter(text_customer=self.kwargs['customer_id']).order_by('-text_message_id')[:10]