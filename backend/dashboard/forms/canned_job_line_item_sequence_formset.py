from homepageapp.models import CannedJobLineItemSequence, CannedJobsNewSQL02Model
from django.forms import inlineformset_factory

CannedJobLineItemSequenceInlineFormset = inlineformset_factory(
    CannedJobsNewSQL02Model,
    CannedJobLineItemSequence,
    fields=('sequence', 'line_item',),
    extra=0,
    can_delete=True,
)
