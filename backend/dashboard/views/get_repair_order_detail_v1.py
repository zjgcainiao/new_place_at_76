from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, messages,redirect, Prefetch
from homepageapp.models import RepairOrdersNewSQL02Model, TextMessagesModel, AddressesNewSQL02Model,NoteItemsNewSQL02Model, PartItemModel,LaborItemModel, VehicleNotesModel
from dashboard.forms import RepairOrderUpdateForm


# dashboard detail view. version 1
# modified to prefetch emails, phones, taxes to each repair_order_customer object

@login_required(login_url='internal_users:internal_user_login')
def get_repair_order_detail_v1(request, pk):

    # Note: Ensure that 'lineitems__lineitem_noteitem' correctly represents the relationship path
    # from your LineItems model to your NoteItems model.
    # Adjust the 'lineitems__lineitem_partitem', 'lineitems__lineitem_laboritem', and
    # 'repair_order_vehicle__vehiclenotes_vehicle' paths as necessary to reflect actual model relationships.

    # Use Prefetch objects for related items to control the queryset used for prefetching
    address_qs = AddressesNewSQL02Model.objects.order_by('address_type_id')
    note_item_qs = NoteItemsNewSQL02Model.objects.all()
    part_item_qs = PartItemModel.objects.all()
    labor_item_qs = LaborItemModel.objects.all()
    vehicle_note_qs = VehicleNotesModel.objects.all()
    text_messages_qs=TextMessagesModel.objects.order_by('-text_message_id')
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses', queryset=address_qs),
        Prefetch('repair_order_customer__phones'),
        Prefetch('repair_order_customer__emails'),
        Prefetch('repair_order_customer__taxes'),
        Prefetch('repair_order_customer__text_customers', queryset=text_messages_qs),
        Prefetch('lineitems__lineitem_noteitem', queryset=note_item_qs),
        Prefetch('lineitems__lineitem_partitem', queryset=part_item_qs),
        Prefetch('lineitems__lineitem_laboritem', queryset=labor_item_qs),
        Prefetch('repair_order_vehicle__vehiclenotes_vehicle', queryset=vehicle_note_qs),
    ).select_related('repair_order_customer', 'repair_order_vehicle').get(pk=pk)

    # repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
    #    Prefetch(
    #        'repair_order_customer__addresses', 
    #         queryset=address_qs),
    #     'repair_order_customer__phones',
    #     'repair_order_customer__emails',
    #     'repair_order_customer__taxes',
    #     'lineitems__lineitem_noteitem',
    #     'lineitems__lineitem_partitem',
    #     'lineitems__lineitem_laboritem',
    #     'repair_order_vehicle__vehiclenotes_vehicle',
    # ).select_related('repair_order_customer',
    #     'repair_order_vehicle'
    #     ).get(pk=pk)
    # repair_order = RepairOrdersNewSQL02Model.objects.get(id=repair_order_id)
    repair_order_id = repair_order.repair_order_id

    if repair_order.repair_order_customer is not None:
        customer = repair_order.repair_order_customer
        # Manually limit the fetched text messages
        text_messages = customer.text_customers.all()[:15]
    else:
        customer = None
        text_messages = None

    if repair_order.repair_order_vehicle is None:
        vehicle = None
    else:
        vehicle = repair_order.repair_order_vehicle

    line_items = repair_order.lineitems.all()
    note_items = [item.lineitem_noteitem.get() for item in line_items if item.lineitem_noteitem.exists()]
    part_items = [item.lineitem_partitem.get() for item in line_items if item.lineitem_partitem.exists()]
    labor_items = [item.lineitem_laboritem.get() for item in line_items if item.lineitem_laboritem.exists()]


    # send out a repair_order_id stored in the request.session.
    request.session['repair_order_id'] = repair_order_id
    # request.session['customer_id'] = customer_id

    if request.method == 'POST':
        # Process form data and save the changes
        form = RepairOrderUpdateForm(request.POST, instance=repair_order)
        if form.is_valid():
            form.save()
            messages.success('redirecting...')
            return redirect('dashboard:repair_order_dash')
    else:
        # Display the form for updating the record
        form = RepairOrderUpdateForm(instance=repair_order)
    # print(f'note_items: {note_items}')
    context = {
        'repair_order': repair_order,
        'form': form,
        'repair_order_id': repair_order_id,
        'note_items': note_items,
        'part_items': part_items,
        'labor_items': labor_items,
        'customer': customer,
        'line_items': line_items,
        'vehicle': vehicle,
        'current_time': CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,
        'text_messages': text_messages,

    }
    return render(request, 'dashboard/21_repair_order_detail_v1.html', context)