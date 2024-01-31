
from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE


@login_required(login_url='internal_users:internal_user_login')
def get_main_dashboard(request):
    # Create the context with the current time.
    context = {
        'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,
    }
    return render(request, 'dashboard/10_main_dashboard.html', context)