from .base import render
from homepageapp.models import LineItemsNewSQL02Model


def technician_dash_view(request, technician_id):
    line_items = LineItemsNewSQL02Model.objects.filter(LineItemTech__id=technician_id).prefetch_related(
        'lineitems__lineitem_noteitem',
        'lineitems__lineitem_laboritem',
        'lineitems__partitems_lineitems',
    )
    return render(request, 'dashboard/technician_workstation.html', {'line_items': line_items})

# this function searchs a vin number entered on the search form. save the most recent snapshot of vehicle info from NHTSA gov website
# to VinNhtsaApiSnapshots model.
