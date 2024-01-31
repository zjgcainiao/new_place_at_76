from .base import forms
from .line_item_update import LineItemUpdateForm

class LineItemCreateForm(LineItemUpdateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id
        del self.fields['line_item_id']

# This liteEmailUpdateForm is used on the customer detail page. It allows users to edit
