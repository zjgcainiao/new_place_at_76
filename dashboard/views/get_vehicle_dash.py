from .base import render, timezone, Paginator
from homepageapp.models import VehiclesNewSQL02Model




def get_vehicle_dash(request):
    vehciles = VehiclesNewSQL02Model.objects.select_related(
        'vehicle_cust',
        'vehicle_brake',
        'vehicle_body_style',
        'vehicle_sub_model',
        'vehicle_make',
        'vehicle_gvw',
        'vehicle_engine',
        'vehicle_brake',
        'vehicle_drive_type',
        'vehicle_transmission',
    ).order_by('-vehicle_id')
    current_time = timezone.now()
    paginator = Paginator(vehciles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 
                  'dashboard/60_vehicle_dash_view.html', 
                  {'page_obj': page_obj,
                    'current_time': current_time,
                    })