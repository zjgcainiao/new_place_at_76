
from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from homepageapp.models import NoteItemsNewSQL02Model
from .automan_base_model import AutomanBaseModelForm


class NoteItemUpdateForm(AutomanBaseModelForm):
    note_item_text = forms.CharField(
        label='Text', 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 3}))
    # note_item_tech_observation = forms.CharField(
    #     label='tech observation', 
    #     required=False, 
    #     widget=forms.TextInput(attrs={'placeholder': 'Enter your tech observation here.'}))
    
    class Meta:
        model = NoteItemsNewSQL02Model
        fields =['note_item_id',
                 'note_item_text', 
                  # 'note_item_tech_observation',
                  ]
        readonly_fields = ['note_item_id',
                           'note_item_created_at', 
                           'note_item_last_updated_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Row(
                Column(Field('note_item_text',css_class='form-control'), css_class='col-12'),
            css_class='form-row p-1 my-1'),
            # note_item_tech_observation is always 0
            # Row(
            #     Column(Field('note_item_tech_observation',css_class='form-control'), css_class='col-12 my-1'),
            # css_class='form-row p-1 my-1'),
        )
