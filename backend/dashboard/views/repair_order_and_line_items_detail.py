
from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, Prefetch
from homepageapp.models import RepairOrdersNewSQL02Model
from dashboard.forms import PartItemInlineFormset, LaborItemInlineFormset


def repair_order_and_line_items_detail(request, repair_order_id):
    repair_order = RepairOrdersNewSQL02Model.objects.prefetch_related(
        Prefetch('repair_order_customer__addresses')).prefetch_related(
        'repair_order_customer__phones',
        'repair_order_customer__emails',
        'repair_order_customer__taxes',
        'lineitems__lineitem_noteitem',
        'lineitems__parts_lineitems',
        'lineitems__lineitem_laboritem',
        'lineitems__lineitem_laboritem').get(pk=repair_order_id)
    line_items = repair_order.lineitems.all()
    part_items = {lineitem.parts_lineitems.all(
    ): lineitem.line_item_id for lineitem in line_items}
    labor_items = {lineitem.lineitem_laboritem.all(
    ): lineitem.line_item_id for lineitem in line_items}
    formset_dict = {}
    formsets = []
    for line_item in line_items:
        formset = PartItemInlineFormset(instance=line_item)
        if formset.total_form_count() == 0:
            formset = LaborItemInlineFormset(instance=line_item)
        formsets.append(formset)
        formset_dict.append({formset: line_item.line_item_id})
    context = {
        'repair_order': repair_order,
        'formsets': formsets,
        'formset_dict': formset_dict,
        'line_items': line_items,
        'part_items': part_items,
        'labor_items': labor_items,
    }
    return render(request, 'dashboard/51_repair_order_line_items.html', context)