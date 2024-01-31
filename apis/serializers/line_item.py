from .base import serializers
from homepageapp.models import LineItemsNewSQL02Model
from .labor_item import LaborItemSerializer
from .part_item import PartItemSerializer
from .note_item import NoteItemSerializer   

class LineItemSerializer(serializers.ModelSerializer):
    laboritems = LaborItemSerializer(many=True, read_only=True)
    noteitems = NoteItemSerializer(many=True, read_only=True)
    partitems = PartItemSerializer(many=True, read_only=True)

    class Meta:
        model = LineItemsNewSQL02Model
        fields = ['line_item_id', 'line_item_type', 'line_item_description',
                   'line_item_cost', 'line_item_sale', 'line_item_is_tax_exempt', 'line_item_has_no_commission', 'line_item_has_fixed_commission', 
                   'line_item_order_revision_id', 'line_item_canned_job', 'line_item_labor_sale', 'line_item_part_sale', 'line_item_part_only_sale', 
                   'line_item_labor_only_sale', 'line_item_sublet_sale', 'line_item_package_sale', 'line_item_tire_fee', 'line_item_parent_line_item', 
                   'line_item_created_at', 'line_item_last_updated_at', 'laboritems', 'noteitems', 'partitems', ]
        read_only_fields = ['line_item_id', 'line_item_created_at', 'line_item_last_updated_at']