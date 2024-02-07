
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from dashboard.forms import LineItemCreateForm, PartItemInlineFormSet, LaborItemInlineFormSet, NoteItemInlineFormSet
from .base import redirect, reverse, InternalUserRequiredMixin,JsonResponse,get_object_or_404,messages

FORMS = [("line_item", LineItemCreateForm),
         ("part_item_formset", PartItemInlineFormSet),
         ("labor_item_formset", LaborItemInlineFormSet),
         ("note_item_formset", NoteItemInlineFormSet)
         ]

TEMPLATES = {"line_item": "dashboard/98_line_item_create_wizard_line_item_form.html",
             "part_item_formset": "dashboard/97_line_item_create_wizard_formsets_partitem.html",
             "labor_item_formset": "dashboard/97_line_item_create_wizard_formsets_laboritem.html",
             "note_item_formset": "dashboard/97_line_item_create_wizard_formsets_noteitem.html"
             }


class LineItemCreateWizard(SessionWizardView,InternalUserRequiredMixin):
    form_list = FORMS
    
    template_name = 'dashboard/96_line_item_create_wizard.html'
    def get_template_names(self):
        # Always use the master template
        return [self.template_name]
        # return [TEMPLATES[self.steps.current]]
                                                                                                                                                      
    def get_form_initial(self, step):
        initial = {}
        if step != 'line_item':
            line_item_data = self.get_cleaned_data_for_step('line_item') or {}
            line_item_type = line_item_data.get('line_item_type') 
            if line_item_type:
                initial['line_item_type'] = line_item_type
        return initial
    
    def get_next_step(self, step=None):
        # Make sure to call the parent's get_next_step to avoid recursion
        next_step = super().get_next_step(step)
        if step != 'line_item':
            line_item_data = self.get_cleaned_data_for_step('line_item') or {}
            line_item_type = line_item_data.get('line_item_type')

            if line_item_type == 'part':
                next_step = 'part_item_formset'
            elif line_item_type == 'labor':
                next_step = 'labor_item_formset'
            elif line_item_type == 'note':
                next_step = 'note_item_formset'
        # Make sure there's a condition to break the recursion
        return next_step

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        current_step = self.steps.current
        # Set the current step template
        context['current_step_template'] = TEMPLATES[current_step]
        print("Current step:", current_step, "Template:", context['current_step_template'])
        
        if self.steps.current != 'line_item':
            line_item_data = self.get_cleaned_data_for_step('line_item') or {}
            line_item_type = line_item_data.get('line_item_type')
            context['line_item_type'] = line_item_type
        
        return context

    # def post(self, *args, **kwargs):
    #     print("Current step before POST:", self.steps.current)
    #     response = super().post(*args, **kwargs)
    #     print("Current step after POST:", self.steps.current)
    #     return response



    def done(self, form_list, **kwargs):
        # Process the line item form
        line_item_form = form_list[0]  # The LineItemCreationForm
        line_item_instance = line_item_form.save()
        # Process the part item formset
        part_item_formset = form_list[1]  # Assuming this is the PartItemInlineFormset
        if part_item_formset.is_valid():
            part_items = part_item_formset.save(commit=False)
            for part_item in part_items:
                part_item.line_item = line_item_instance  # Set the foreign key to the line item
                part_item.save()

        # Similar logic for labor items and note items
        
        # Save the LineItem and the associated items based on the selected formset
        messages.info(self.request, 'creating...')
        return render(self.request, 'dashboard/96_line_item_create_wizard.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
