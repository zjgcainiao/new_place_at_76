from django.urls import reverse
from .base import render
from homepageapp.models import LineItemsNewSQL02Model, RepairOrdersNewSQL02Model
from django.contrib.auth.decorators import login_required
from internal_users.models import InternalUser
from dashboard.forms import LineItemChecklistForm
# internal_user_login_url = reverse('internal_users:internal_user_login')
from django.contrib.auth.decorators import login_required, user_passes_test


def is_technical(user):
    return user.groups.filter(name='Technical').exists()


@login_required
@user_passes_test(is_technical)
def some_technical_view(request):
    # Only accessible to users in the 'Technical' group
    return render(request, 'technical_page.html')


@login_required(login_url='employees/login')
def technician_dash_view(request):
    if isinstance(request.user, InternalUser):
        asggined_to = request.user
    repair_order = RepairOrdersNewSQL02Model.objects.filter(
        repair_order_id=123628)

    # line_item_checklist_form = LineItemChecklistForm(line_items=line_items)

    line_items = LineItemsNewSQL02Model.objects.filter(
        assigned_to=asggined_to,
    ).prefetch_related(
        'lineitems__lineitem_noteitem',
        'lineitems__lineitem_laboritem',
        'lineitems__lineitem_partitem',
        'lineitems__lineitem_partitem__part_item_part',
    )
    return render(request, 'dashboard/70_technician_dash.html',
                  {'line_items': line_items})

# this function searchs a vin number entered on the search form.
# save the most recent snapshot of vehicle info from NHTSA gov website
# to VinNhtsaApiSnapshots model.
