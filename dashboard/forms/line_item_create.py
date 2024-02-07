from .base import forms
from .line_item_update import LineItemUpdateForm


class LineItemCreateForm(LineItemUpdateForm):
    LINE_ITEM_TYPES = [
        ('part', 'Part Item'),
        ('labor', 'Labor Item'),
        ('note', 'Note Item'),
        # ('cannedjob', 'Canned Job'),
    ]
    line_item_type = forms.ChoiceField(
        choices=LINE_ITEM_TYPES,
        required=True,
        disabled=False,
    )
    line_item_description = forms.CharField(widget=forms.Textarea(
        attrs={"type": "text",
                "rows": 3,
                "style": "overflow-y: scroll;"}), 
                label='Brief Desc.',
                required=False,
                )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta(LineItemUpdateForm.Meta):
        fields = LineItemUpdateForm.Meta.fields + ['line_item_type']

        # exclude the line item id
        # del self.fields['line_item_id']
        # This liteEmailUpdateForm is used on the customer detail page. It allows users to edit
