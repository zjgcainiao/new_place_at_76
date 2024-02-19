from homepageapp.models import CannedJobLineItemSequence, CannedJobsNewSQL02Model
from django.forms import inlineformset_factory
from .canned_job_line_item_sequence import CannedJobLineItemSequenceForm

CannedJobLineItemSequenceInlineFormset = inlineformset_factory(
    CannedJobsNewSQL02Model,
    CannedJobLineItemSequence,
    form=CannedJobLineItemSequenceForm,
    fields=('sequence', 'line_item_id', 'line_item_description', 
            'line_item_cost', 'line_item_sale', 'line_item_has_fixed_commission', 'line_item_is_tax_exempt'),
    fk_name='canned_job',
    extra=0,
    can_delete=True,
)
