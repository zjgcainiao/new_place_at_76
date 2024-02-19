
from .base import forms,FormHelper,Layout,Field,Fieldset,Submit,ButtonHolder,HTML,Reset,Column,Row,Div,Button,Hidden
from .automan_base_model import AutomanBaseModelForm

from homepageapp.models import CannedJobLineItemSequence, CannedJobsNewSQL02Model, CategoryModel

class CannedJobUpdateForm(forms.ModelForm):

    canned_job_title = forms.CharField(required=True, 
                                       label='Title',
                                       widget=forms.TextInput(attrs={}))
    canned_job_is_in_quick_menu = \
        forms.BooleanField(required=False, 
            widget=forms.CheckboxInput(attrs={'class': 'toggle-switch'}), 
            label='Included in Quick Menu?')
    
    canned_job_category = forms.ModelChoiceField(queryset=CategoryModel.objects.all(),
                                                    required=False,
                                                    label='Category')
    canned_job_description = forms.CharField(required=True,
                                             label=' Description',
                                             widget=forms.TextInput(attrs={}))
    canned_job_applied_year = forms.CharField(required=False,
                                              label='Applied Year (if applicable)',
                                              widget=forms.TextInput(attrs={}))
    class Meta:
        model = CannedJobsNewSQL02Model
        fields = [
            'canned_job_title',
            'canned_job_description',
            'canned_job_is_in_quick_menu',
            'canned_job_category',
            'canned_job_applied_year',
        ]
        readonly_fields = ['canned_job_id', 'canned_job_created_at', 'canned_job_last_updated_at', 'created_by', 'modified_by']

            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_clsas = 'form-inline'
        self.helper.layout = Layout(
            Field('canned_job_title', wrap_class='form-group'),
            'canned_job_description',
            Field('canned_job_is_in_quick_menu',wrap_class=''), 
            'canned_job_category',
            'canned_job_applied_year',
        )