
from formtools.wizard.views import SessionWizardView
from django import forms
from django.shortcuts import render
from dashboard.forms import LineItemCreateForm, PartItemInlineFormSet, LaborItemInlineFormSet, NoteItemInlineFormSet
from .base import redirect, reverse, InternalUserRequiredMixin,JsonResponse,get_object_or_404,messages

# FORMS = [("line_item", LineItemCreateForm),
#          ("selected_formset", [PartItemInlineFormSet,LaborItemInlineFormSet,NoteItemInlineFormSet]),
#          ("labor_item_formset", LaborItemInlineFormSet),
#          ("note_item_formset", NoteItemInlineFormSet)
#          ]


# TEMPLATES = {"line_item": "dashboard/98_line_item_create_wizard_line_item_form.html",
#              "selected_formset": "dashboard/97_line_item_create_wizard_formsets.html",
#              "labor_item_formset": "dashboard/97_line_item_create_wizard_formsets.html",
#              "note_item_formset": "dashboard/97_line_item_create_wizard_formsets.html"
#              }

FORMS = [
    ("line_item", LineItemCreateForm),
    ("selected_formset", forms.Form),  # Placeholder, actual formset determined in get_form
]

TEMPLATES = {"line_item": "dashboard/98_line_item_create_wizard_line_item_form.html",
             "selected_formset": "dashboard/97_line_item_create_wizard_formsets.html",
             }

class LineItemCreateWizard(SessionWizardView,InternalUserRequiredMixin):
    form_list = FORMS
    
    template_name = 'dashboard/96_line_item_create_wizard.html'
    def get_template_names(self):
        # Always use the master template
        return [self.template_name]
        # return [TEMPLATES[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        # Dynamically determine the formset for the 'selected_formset' step
        if step == 'selected_formset':
            line_item_data = self.get_cleaned_data_for_step('line_item') or {} # line_item_type and `brief description` field
            line_item_type = line_item_data.get('line_item_type')

            # Select the formset based on line_item_type
            if line_item_type == 'part':
                form_class = PartItemInlineFormSet
            elif line_item_type == 'labor':
                form_class = LaborItemInlineFormSet
            elif line_item_type == 'note':
                form_class = NoteItemInlineFormSet
            else:
                # Fallback or error handling
                form_class = forms.Form  # Use a blank form as fallback
            
            # Initialize and return the formset
            return form_class(**self.get_form_kwargs(step))

            # For steps other than 'selected_formset', use the default behavior
        return super().get_form(step, data, files)

    # def get_form_initial(self, step):
    #     initial = {}
    #     if step != 'line_item':
    #         line_item_data = self.get_cleaned_data_for_step('line_item') or {}
    #         line_item_type = line_item_data.get('line_item_type') 
    #         if line_item_type:
    #             initial['line_item_type'] = line_item_type
    #     return initial

    # def get_next_step(self, step=None):
    #     # Make sure to call the parent's get_next_step to avoid recursion
    #     next_step = super().get_next_step(step)
        # if step != 'line_item':
        #     line_item_data = self.get_cleaned_data_for_step('line_item') or {}
        #     line_item_type = line_item_data.get('line_item_type')

        #     if line_item_type == 'part':
        #         next_step = 'selected_formset'
        #     elif line_item_type == 'labor':
        #         next_step = 'labor_item_formset'
        #     elif line_item_type == 'note':
        #         next_step = 'note_item_formset'
        # Make sure there's a condition to break the recursion
        # return next_step

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
        selected_formset = form_list[1]  # Assuming this is the PartItemInlineFormset
        if selected_formset.is_valid():
           sub_items = selected_formset.save(commit=False)
           for sub_item in sub_items:
                sub_item.line_item = line_item_instance  # Set the foreign key to the line item
                sub_item .save()

        form_data = [form.cleaned_data for form in form_list]
        
        # Save the LineItem and the associated items based on the selected formset
        messages.info(self.request, 'creating a new line item is successful')
        return render(self.request, 'dashboard/96_line_item_create_wizard.html', {
            'form_data': form_data,
        })
