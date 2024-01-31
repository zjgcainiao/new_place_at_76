
from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from homepageapp.models import NoteItemsNewSQL02Model
from .automan_base_model import AutomanBaseModelForm


class NoteItemUpdateForm(AutomanBaseModelForm):

    class Meta:
        model = NoteItemsNewSQL02Model
        fields =['note_item_id','note_item_text', 
                 'note_item_tech_observation', ]
        readonly_fields = ['note_item_id','note_item_created_at', 'note_item_last_updated_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control text-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control textarea-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'custom-select'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'datetime-input'})
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"

            # You can continue for other field types
