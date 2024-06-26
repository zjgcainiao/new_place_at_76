from .base import render, login_required, CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE,messages,redirect,get_object_or_404
from homepageapp.models import LineItemsNewSQL02Model
from dashboard.forms import PartItemInlineFormset, LaborItemInlineFormset, NoteItemInlineFormset, LineItemUpdateForm


# 2024-01-21 this is the current version of the line item update merge view
def line_item_merge_view(request, pk, line_item_id):
    repair_order_id = pk  # pk is repair_order_id in repairorder model.
    # Fetch the line item without prefetching
    line_item = get_object_or_404(
        LineItemsNewSQL02Model.objects.prefetch_related(
            'lineitem_partitem', 'lineitem_laboritem', 'lineitem_noteitem'
        ),
        line_item_id=line_item_id
    )
    if not line_item:
        messages.error(f'Cannot find the line item by its given id {line_item_id}.')
        return redirect('dashboard:get_repair_order_detail_v1', pk=pk)
    # use .all() instead of .exists() to reduce the number of queries into DB.
    if line_item.line_item_type == 'part':
        Formset = PartItemInlineFormset
    elif line_item.line_item_type == 'labor':
        Formset = LaborItemInlineFormset
    elif line_item.line_item_type == 'note':
        Formset = NoteItemInlineFormset
    else:
        Formset = None
        messages.warning(request,
                       f'error fetching labor or part item information for line item {line_item_id}. data empty or not found.')
        return redirect('dashboard:get_repair_order_detail_v1', pk=pk)

    
    # in one single line item, some data is from lineitem table, some is either from partitem or laboritem table.
    if request.method == 'POST':
        form = LineItemUpdateForm(request.POST, instance=line_item)
        formset = Formset(request.POST, instance=line_item)

        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            messages.success(
                request, 'Line items have been updated successfully!')
            return redirect('dashboard:get_repair_order_detail_v1', pk=pk)
    else:
        formset = Formset(instance=line_item)
        form = LineItemUpdateForm(instance=line_item)

    context = {
        'formset': formset,
        'form': form,
        'repair_order_id': repair_order_id,
        'line_item_id': line_item_id,
        'line_item': line_item,
    }
    return render(request, 'dashboard/93_part_labor_item_update_view_v2.html', context)
