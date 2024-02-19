from .base import forms, TalentsModel
from .personal_contact_info import PersonalContactInfoForm
from .employment_info import EmploymentInfoForm
class RemarkAndCommentsForm(forms.ModelForm):

    class Meta:
        model = TalentsModel
        # Replace with the actual fields you want to display in the Contact Info section
        fields = ['talent_HR_remarks_json', 'talent_incident_record_json',]
        labels = {'talent_HR_remarks_json': 'Incident Records in JSON format',
                  'talent_incident_record_json': 'Company Comments in JSON format',
                  }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

