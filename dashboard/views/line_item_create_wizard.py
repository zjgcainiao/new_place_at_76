
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from dashboard.forms import LineItemCreateForm, PartItemInlineFormSet, LaborItemInlineFormSet, NoteItemInlineFormSet
from .base import redirect, reverse, InternalUserRequiredMixin,JsonResponse,get_object_or_404,messages

FORMS = [("line_item", LineItemCreateForm),
         ("part_item_formset", PartItemInlineFormSet),
         ("labor_item_formset", LaborItemInlineFormSet),
         ("note_item_formset", NoteItemInlineFormSet)]

TEMPLATES = {"line_item": "dashboard/98_line_item_create_wizard_line_item_form.html",
             "part_item_formset": "dashboard/97_line_item_create_wizard_formsets_partitem.html",
             "labor_item_formset": "dashboard/97_line_item_create_wizard_formsets_laboritem.html",
             "note_item_formset": "dashboard/97_line_item_create_wizard_formsets_noteitem.html"}


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
                initial.update({'line_item_type': line_item_type})
        return initial

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        current_step = self.steps.current
        # Set the current step template
        context['current_step_template'] = TEMPLATES[current_step]
        print("Current step template:", context['current_step_template'])
        
        if self.steps.current != 'line_item':
            line_item_data = self.get_cleaned_data_for_step('line_item') or {}
            line_item_type = line_item_data.get('line_item_type')
        
        return context

    def done(self, form_list, **kwargs):
        # Process the submitted forms
        # Save the LineItem and the associated items based on the selected formset
        messages.info(self.request, 'creating...')
        return render(self.request, 'dashboard/96_line_item_create_wizard.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
