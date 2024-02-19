from .base import render, timezone, Paginator
from homepageapp.models import CannedJobsNewSQL02Model
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE



def get_canned_job_dash(request):
    canned_jobs = CannedJobsNewSQL02Model.objects.select_related(
        'canned_job_category',
        'created_by',
        'modified_by',

    ).order_by('-canned_job_is_in_quick_menu','canned_job_title',)
    current_time = CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
    paginator = Paginator(canned_jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 
                  'dashboard/50_canned_job_dash.html', 
                  {'page_obj': page_obj,
                    'current_time': current_time,
                    })