
from .base import forms,FormHelper,Layout,Field,Fieldset,Submit,ButtonHolder,HTML,Reset,Column,Row,Div,Button,Hidden
from .automan_base_model import AutomanBaseModelForm

from homepageapp.models import CannedJobLineItemSequence, CannedJobsNewSQL02Model

class CannedJobUpdateForm(AutomanBaseModelForm):
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
        self.helper.layout = Layout(
            'canned_job_title',
            'canned_job_description',
            Field('canned_job_is_in_quick_menu', wrap_class='form-switch'),
            'canned_job_category',
            'canned_job_applied_year',
        )