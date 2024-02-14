from .base import render, login_required, get_object_or_404,reverse, redirect,messages
from homepageapp.models import LineItemsNewSQL02Model
from dashboard.forms import PartItemInlineFormset, LaborItemInlineFormset, NoteItemInlineFormset, LineItemUpdateForm

def line_item_three_in_one_update(request, pk, line_item_id):
    repair_order_id = pk # pk is repair_order_id in repairorder model.
    # lineitem = get_object_or_404(LineItemsNewSQL02Model.objects.filter(pk=line_item_id))
    lineitem = get_object_or_404(
        LineItemsNewSQL02Model.objects.prefetch_related(
            'lineitem_partitem', 
            'lineitem_laboritem', 
            'lineitem_noteitem'
        ),
        pk=line_item_id
    )
    line_item_type = lineitem.line_item_type or None

    form = LineItemUpdateForm(request.POST or None, instance=lineitem)
    formset_class = None
    if line_item_type == 'part':
        formset_class = PartItemInlineFormset
    elif line_item_type == 'labor':
        formset_class = LaborItemInlineFormset
    elif line_item_type == 'note':
        formset_class = NoteItemInlineFormset

    if request.method == "POST":
            if formset_class:
                selected_formset = formset_class(request.POST, instance=lineitem)
                if form.is_valid() and selected_formset.is_valid():
                    # Save the form and formset
                    form.save()
                    selected_formset.save()
                    messages.success(request, 'Line item updated successfully.')
                    # Redirect to a new URL using the redirect shortcut
                    return redirect('dashboard:repair_item_detail', pk=repair_order_id)
            else:
                if form.is_valid():
                    form.save()
                    # Redirect if there's no formset but the main form is valid
                    return redirect('dashboard:line_item_detail', pk=repair_order_id)
    else:
        if formset_class:
            selected_formset = formset_class(instance=lineitem)
        else:
           selected_formset = None  # Handle the case where no formset is needed

    context = {
        'repair_order_id': repair_order_id,
        'selected_formset': selected_formset,
        'form': form, # LineItemUpdateForm
        'line_item_id': line_item_id,

    }
    return render(request, 'dashboard/95_line_item_three_in_one_update.html', context)
