
from .base import LoginRequiredMixin, get_object_or_404, reverse, UpdateView
from homepageapp.models import LineItemsNewSQL02Model
from dashboard.forms import PartItemUpdateForm, PartItemInlineFormSet, LaborItemInlineFormSet



class LineItemUpdateView(UpdateView, LoginRequiredMixin):
    # template_name = 'dashboard/90_part_item_list_view.html'
    template_name = 'dashboard/92_part_labor_item_update_view.html'
    form_class = PartItemUpdateForm
    context_object_name = 'line_item_part_or_labor'

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # qs = qs.prefetch_related('repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
        #        ).prefetch_related('repair_order_customer__taxes').prefetch_related('lineitems__parts_lineitems').prefetch_related('lineitems__lineitem_laboritem')
        qs = LineItemsNewSQL02Model.objects.prefetch_related(
            'partitems_lineitems').prefetch_related('lineitem_laboritem')
        # repair order phase defines the WIP (work-in-progress) category. 6 means invoice.  7 counter sale. 8 deleted. 9 scheduled.
        # qs = qs.filter(Q(repair_order_phase=1) | Q(repair_order_phase=2) | Q(repair_order_phase=3) | Q(repair_order_phase=4) | Q(repair_order_phase=5))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        line_item = get_object_or_404(
            LineItemsNewSQL02Model, pk=self.kwargs['line_item_id'])
        if line_item is not None:
            part_item_formset = PartItemInlineFormSet(instance=line_item)
            labor_item_formset = LaborItemInlineFormSet(instance=line_item)
            if labor_item_formset.empty_form:
                selected_formset = part_item_formset
            else:
                selected_formset = labor_item_formset
        context['selected_formset'] = selected_formset
        context['part_item_formset'] = part_item_formset
        context['labor_item_formset'] = labor_item_formset
        # try:
        #     part_item = line_item.parts_lineitems.first()
        #     form = PartItemModelForm(instance=part_item)
        #     # part_item = get_object_or_404(PartItemModel,pk=self.kwargs['line_item_id'])
        # except ObjectDoesNotExist:
        #     # return redirect(reverse('dashboard:labor-item-update-view', kwargs=self.kwargs))
        #     labor_item = line_item.lineitem_laboritem.first()
        #     form = LaborItemModelForm(instance=labor_item)

        context['page_title'] = 'Update a Line Item'
        # context['form'] = form
        context['fields'] = self.get_form().fields.items()
        # the line_item_id in the url pattern is passed on to the Updateview .
        context['line_item_id'] = self.kwargs['line_item_id']
        # the pk in the url pattern is passed on to the UpdateView .
        context['repair_order_id'] = self.kwargs['pk']
        context['line_item'] = line_item
        return context

    # def form_valid(self,form):
    #     response = super().form_valid(form)
    #     return redirect(reverse('dashboard:dashboard_detail',args=self.kwargs['line_item_id']))