from .base import get_object_or_404, redirect, render,reverse
from homepageapp.models import CannedJobsNewSQL02Model, CannedJobLineItemSequence
from dashboard.forms import CannedJobUpdateForm, CannedJobLineItemSequenceInlineFormset

def canned_job_update(request, pk):
    canned_job = get_object_or_404(CannedJobsNewSQL02Model, pk=pk)
    form = CannedJobUpdateForm(request.POST or None, instance=canned_job)
    if request.method == 'POST':
        formset = CannedJobLineItemSequenceInlineFormset(request.POST, instance=canned_job)
        if formset.is_valid():
            formset.save()
            # Redirect or indicate success as necessary
    else:
        formset = CannedJobLineItemSequenceInlineFormset(instance=canned_job)
    
    return render(request, 'dashboard/52_canned_job_update.html', {
        'form': form,
        'formset': formset,
    })