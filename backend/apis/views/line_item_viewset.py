from .base import viewsets, IsAuthenticated, IsInternalUser, Response, status
from apis.serializers import LineItemSerializer
from homepageapp.models import LineItemsNewSQL02Model

class LineItemsViewSet(viewsets.ModelViewSet):

    serializer_class = LineItemSerializer
    permission_classes = [IsAuthenticated, IsInternalUser]
    # override the get_queryset method to prefetch related data. this step is important to improve querying performance.
    def get_queryset(self):
        return LineItemsNewSQL02Model.objects.prefetch_related(
            'lineitem_laboritem',  # Related name for LaborItemModel
            'lineitem_noteitem',   # Related name for NoteItemModel
            'partitems_lineitems'  # Related name for PartItemModel
        )
# get the most recent 10 text messages
