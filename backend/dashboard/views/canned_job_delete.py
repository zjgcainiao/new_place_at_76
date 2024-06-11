from .base import get_object_or_404, redirect, render, reverse, messages
from homepageapp.models import CannedJobsNewSQL02Model


def canned_job_delete(request, pk):
    canned_job = get_object_or_404(CannedJobsNewSQL02Model, pk=pk)
    # canned_job_id=pk
    if request.method == 'POST':
        canned_job.delete()
        messages.success(request, 'Canned Job deleted successfully')
        return redirect(reverse('dashboard:canned_job_dash'))
    return render(request,
                  'dashboard/53_canned_job_delete.html',
                  {'canned_job': canned_job})
