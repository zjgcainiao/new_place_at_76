from .base import get_object_or_404, redirect, render,reverse,messages
from homepageapp.models import CannedJobsNewSQL02Model, CannedJobLineItemSequence
from dashboard.forms import CannedJobUpdateForm, CannedJobLineItemSequenceInlineFormset

def canned_job_update(request, pk):
    canned_job = get_object_or_404(CannedJobsNewSQL02Model, pk=pk)
    sequences = CannedJobLineItemSequence.objects.filter(canned_job=canned_job).select_related('line_item').order_by('sequence')

    if request.method == 'POST':
        form = CannedJobUpdateForm(request.POST, instance=canned_job)
        formset = CannedJobLineItemSequenceInlineFormset(request.POST, instance=canned_job)
        if formset.is_valid() and form.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Canned Job updated successfully')
            return redirect(reverse('dashboard:canned_job_detail', args=[canned_job.pk]))
    else:
        form = CannedJobUpdateForm(instance=canned_job)
        # Initialize the formset with a queryset ordered by 'sequence'
        # formset_queryset = CannedJobLineItemSequence.objects.filter(canned_job=canned_job).order_by('sequence')
        formset = CannedJobLineItemSequenceInlineFormset(instance=canned_job, queryset=sequences )
    
    
    return render(request, 'dashboard/52_canned_job_update.html', {
        'form': form,
        'formset': formset,
        'pk': pk,
    })