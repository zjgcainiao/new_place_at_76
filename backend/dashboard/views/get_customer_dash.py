from .base import render, login_required, get_object_or_404, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, Paginator
from homepageapp.models import CustomersNewSQL02Model



def get_customer_dash(request):
    # customer_is_activate=False means that a customer is not deactivated. the name of this field is confusing. will
    # need to revise it before PROD launch.
    active_customers = CustomersNewSQL02Model.objects.filter(
        customer_is_deleted=False).prefetch_related(
        'vehicle_customers',
        'addresses',
        'phones',
        'emails',
    )

    current_time = CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
    paginator = Paginator(active_customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/40_customer_dash_view.html', {'page_obj': page_obj,
                                                                    'current_time': current_time,
                                                                    })
