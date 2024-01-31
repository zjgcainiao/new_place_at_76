from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, messages,redirect, Prefetch
from homepageapp.models import RepairOrdersNewSQL02Model, TextMessagesModel
from dashboard.forms import RepairOrderUpdateForm


# dashboard detail view. version 1
# modified to prefetch emails, phones, taxes to each repair_order_customer object

@login_required(login_url='internal_users:internal_user_login')
def get_wip_dash_detail_v1(request, pk):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses'),
        'repair_order_customer__phones',
        'repair_order_customer__emails',
        'repair_order_customer__taxes',
        'lineitems__lineitem_noteitem',
        'lineitems__partitems_lineitems',
        'lineitems__lineitem_laboritem',
    ).select_related('repair_order_customer','repair_order_vehicle').get( # select_related
        pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_id = repair_order.repair_order_id
    customer_id = repair_order.repair_order_customer.customer_id
    vehicle = repair_order.repair_order_vehicle

    line_items = repair_order.lineitems.all()

    text_messages = TextMessagesModel.objects.filter(
        text_customer=customer_id).order_by('-text_message_id')[:10]

    # send out a repair_order_id stored in the request.session.
    request.session['repair_order_id'] = repair_order_id
    # request.session['customer_id'] = customer_id

    if request.method == 'POST':
        # Process form data and save the changes
        form = RepairOrderUpdateForm(request.POST, instance=repair_order)
        if form.is_valid():
            form.save()
            messages.success('redirecting...')
            return redirect('dashboard:wip_dash')
    else:
        # Display the form for updating the record
        form = RepairOrderUpdateForm(instance=repair_order)

    context = {
        'repair_order': repair_order,
        'form': form,
        'repair_order_id': repair_order_id,
        'customer_id': customer_id,
        'line_items': line_items,
        'vehicle': vehicle,
        'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,
        'text_messages': text_messages,

    }
    return render(request, 'dashboard/21_dashboard_detail.html', context)