from .base import render, login_required, get_object_or_404, redirect, messages
from homepageapp.models import LineItemsNewSQL02Model
from dashboard.forms import PartItemInlineFormSet, LaborItemInlineFormSet, NoteItemInlineFormSet, LineItemUpdateForm, LineItemCreateForm


def line_item_three_in_one_create(request, pk):
    repair_order_id = pk # pk is repair_order_id in repairorder model.
    if request.method == 'POST':
        form = LineItemUpdateForm(request.POST)

        line_item_type = request.POST.get('line_item_type')
        if line_item_type == 'part':
            selected_formset = PartItemInlineFormSet
        elif line_item_type == 'labor':
            selected_formset = LaborItemInlineFormSet
        elif line_item_type == 'note':
            selected_formset = NoteItemInlineFormSet
        else:
            selected_formset = None

        formset = selected_formset(request.POST)

        formset = selected_formset(request.POST) if selected_formset else None
        if form.is_valid() and (formset is None or formset.is_valid()):
            line_item = form.save(commit=False)
            # line_item.line_item_type = line_item_type
            line_item.save()

            if formset:
                instances = formset.save(commit=False)
                for instance in instances:
                    # associate_instance_with_line_item(instance, line_item)
                    instance.save()
                messages.success(request, 'A work item were created successfully.')
            return redirect('dashboard:wip_dash_detail_v1', pk=repair_order_id)

        else:
            form = LineItemCreateForm()
            selected_formset = None

        return render(request, 'dashboard/94_line_item_three_in_one_create.html', {
            'form': form,
            'selected_formset': selected_formset,
        })