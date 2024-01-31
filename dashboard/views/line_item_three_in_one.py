from .base import render, login_required, get_object_or_404
from homepageapp.models import LineItemsNewSQL02Model
from dashboard.forms import PartItemInlineFormSet, LaborItemInlineFormSet, NoteItemInlineFormSet, LineItemUpdateForm

def lineitem_three_in_one_view(request, pk, line_item_id):
    repair_order_id = pk # pk is repair_order_id in repairorder model.
    # lineitem = get_object_or_404(LineItemsNewSQL02Model.objects.filter(pk=line_item_id))
    lineitem = get_object_or_404(
        LineItemsNewSQL02Model.objects.prefetch_related(
            'partitems_lineitems', 
            'lineitem_laboritem', 
            'lineitem_noteitem'
        ),
        pk=line_item_id
    )
    line_item_type = lineitem.line_item_type or None
    if line_item_type == 'part':
        selected_formset = PartItemInlineFormSet
    elif line_item_type == 'labor':
        selected_formset = LaborItemInlineFormSet
    elif line_item_type == 'note':
        selected_formset = NoteItemInlineFormSet
    else:
        selected_formset = None

    if request.method == "POST":
        form = LineItemUpdateForm(request.POST, instance=lineitem)
        # Create formset instances and save them
        pass
    else:
        form = LineItemUpdateForm(instance=lineitem)
        selected_formset = selected_formset(instance=lineitem)
    context = {
        'repair_order_id': repair_order_id,
        'selected_formset': selected_formset,
        'form': form,

    }
    return render(request, 'dashboard/94_part_labor_note_formsets.html', context)