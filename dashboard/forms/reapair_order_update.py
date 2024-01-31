from .base import forms 
from homepageapp.models import RepairOrdersNewSQL02Model


class RepairOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = [
            'repair_order_customer',
            'repair_order_phase',
            'repair_order_created_as_estimate',
            'repair_order_is_printed',
            'repair_order_aggr_notes',
            'repair_order_snapshot_order_total_amount',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
