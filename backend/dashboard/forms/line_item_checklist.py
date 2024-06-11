from django import forms
from homepageapp.models import PartItemModel, LaborItemModel, \
        LineItemsNewSQL02Model, NoteItemsNewSQL02Model

class LineItemChecklistForm(forms.Form):
    def __init__(self, *args, **kwargs):
        line_items = kwargs.pop('line_items', [])
        super().__init__(*args, **kwargs)
        for item in line_items:
            self.fields[f'item_completed_{item.id}'] = forms.BooleanField(label=item.line_item_description, required=False)
            # if isinstance(item, PartItemModel):
            #     # Add specific logic or fields for PartItems
            #     self.fields[field_key] = forms.BooleanField(label=f'Check Part: {item.description} ({item.service_type})', required=False)
            # elif isinstance(item, LaborItemModel):
            #     # Add specific logic or fields for LaborItems
            #     self.fields[field_key] = forms.BooleanField(label=f'Check Labor: {item.description} ({item.service_type})', required=False)
            # elif isinstance(item, NoteItemsNewSQL02Model):
            #     # Add specific logic or fields for NoteItems
            #     self.fields[field_key] = forms.BooleanField(label=f'Check Note: {item.description} ({item.service_type})', required=False)
