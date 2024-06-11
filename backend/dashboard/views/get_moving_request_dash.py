from .base import render, timezone,  logger, \
    Paginator,  PageNotAnInteger, EmptyPage, \
    messages

from homepageapp.models import MovingRequest
from core_operations.constants import DEFAULT_PAGE_SIZE, \
    DEFAULT_PAGE_SIZE_LARGE


def get_moving_request_dash(request):
    items = MovingRequest.objects.prefetch_related(
        'moving_items',
        'moving_items__moving_item',
        'moving_items__container',
        'moving_items__status',
        'moving_items__created_at',
        'moving_items__updated_at',
    ).filter(
        is_active=True
    ).order_by('-move_date')

    current_time = timezone.now()
    paginator = Paginator(items,  DEFAULT_PAGE_SIZE)
    page_number = request.GET.get('page')
    try:
        items = MovingRequest.objects.prefetch_related(
            'moving_items',  # Corrected to just 'moving_items' since it's the related_name
            'moving_items__container',  # Assuming 'container' is a field in MovingItem
        ).filter(
            is_active=True  # Assuming there is an 'is_active' field in MovingRequest
        ).order_by('-move_date')

        current_time = timezone.now()
        paginator = Paginator(items, DEFAULT_PAGE_SIZE)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request,
                      'dashboard/110_moving_request_dash.html',
                      {'page_obj': page_obj,
                       'current_time': current_time,
                       })

    except Exception as e:
        # Log the error or send it to your monitoring system
        logger.error(f"Error fetching moving requests: {str(e)}")
        messages.error(request, f'Error fetching moving requests: {str(e)}')
        # You may decide to show a generic error message or redirect to an error page
        return render(
            request,
            'dashboard/110_moving_request_dash.html',
            {'error': str(e)}
        )
