from .base import render, timezone, Paginator
from homepageapp.models import PersonalItem
from core_operations.constants import DEFAULT_PAGE_SIZE, \
    DEFAULT_PAGE_SIZE_LARGE


def get_personal_item_dash(request):
    items = PersonalItem.objects.filter(
        is_active=True
    ).order_by('item_category', '-id')
    current_time = timezone.now()
    paginator = Paginator(items,  DEFAULT_PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'dashboard/100_personal_item_dash.html',
                  {'page_obj': page_obj,
                   'current_time': current_time,
                   })
