from .base import forms, date_format, \
    FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from .automan_base_model import AutomanBaseModelForm
from homepageapp.models import LineItemsNewSQL02Model, CategoryModel

class LineItemUpdateForm(AutomanBaseModelForm):
    LINE_ITEM_TYPES = [
        ('part', 'Part Item'),
        ('labor', 'Labor Item'),
        ('note', 'Note Item'),
        # ('cannedjob', 'Canned Job'),
    ]

    line_item_type = forms.ChoiceField(
        choices=LINE_ITEM_TYPES,
        label='Item Type',
        disabled=True,
    )

    # line_item_category = forms.ModelChoiceField(
    #     queryset=CategoryModel.objects.all(),
    #     required=False,
    #     label='category',
    #     to_field_name="category_description",
    
    line_item_description = forms.CharField(
        widget=forms.Textarea(
            attrs={"type": "text",
                    "rows": 1,
                    "style": "overflow-y: scroll;",
                    "placeholder": "If its a part,describe the part briefly. if its a labor, describe what is being done in short words. if it is a tech note, adivse what is being done or what is needed."
                    }), 
            label='Brief Desc.',
            required=False,
        ),
    class Meta:
        model = LineItemsNewSQL02Model
        fields = [
            'line_item_type',
            'line_item_description',
            # 'line_item_category',
            'line_item_parent_line_item',
        ]
        exclude = ['line_item_id']
        # readonly_fields = ['line_item_id','line_item_parent_line_item','line_item_last_updated_at','line_item_created_at' ]
        # exclude = [
        #     'line_item_parent_line_item_id',]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # Set the queryset
        # self.fields['line_item_category'].queryset = CategoryModel.objects.all()

        # Set disabled fields
        # instance = kwargs.get('instance', None)
        # if instance:
        #     # Disabling certain fields
        #     # self.fields['line_item_id'].disabled = True
        #     self.fields['line_item_parent_line_item'].disabled = True

        instance = kwargs.get('instance', None)

        # Formulate the HTML strings with actual values if the instance exists
        id_html = '' if not instance else '<p><strong>ID:</strong> {}</p>'.format(instance.line_item_id)
        created_at_html = ''
        updated_at_html = ''

        if instance and instance.line_item_created_at:
            # Format the datetime object to a string as per the specified format
            created_at_str = date_format(instance.line_item_created_at, "Y-m-d P")
            created_at_html = f'<p><strong>Created At:</strong> {created_at_str}</p>'

        if instance and instance.line_item_last_updated_at:
            updated_at_str = date_format(instance.line_item_last_updated_at, "Y-m-d P")
            updated_at_html = f'<p><strong>Last Updated At:</strong> {updated_at_str}</p>'

        parent_line_item_html = '' if not instance or not instance.line_item_parent_line_item else '<p><strong>Parent Line Item:</strong> {}</p>'.format(instance.line_item_parent_line_item)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Row(
                Column(HTML(id_html), css_class='col-4'),
                Column(HTML(updated_at_html), css_class='col-4'),
                Column(HTML(created_at_html), css_class='col-4'),
                Column(HTML(parent_line_item_html), css_class='col-12'),
            css_class='p-1 my-1'),
            Row(
                Column(Field('line_item_type',css_class='form-select'), css_class='col-3 '),
                Column(Field('line_item_description',css_class='form-control'), css_class='col-12'),

            css_class='form-group p-1 my-1'),

        )