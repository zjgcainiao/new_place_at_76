from .base import forms, FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden
from .automan_base_model import AutomanBaseModelForm
from homepageapp.models import LineItemsNewSQL02Model, CategoryModel

class LineItemUpdateForm(AutomanBaseModelForm):
    LINE_ITEM_TYPES = [
        ('part', 'Part Item'),
        ('labor', 'Labor Item'),
        ('note', 'Note Item'),
        ('cannedjob', 'Canned Job'),
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
    line_item_description = forms.CharField(widget=forms.Textarea(
        attrs={"type": "text",
                "rows": 3,
                "style": "overflow-y: scroll;"}), 
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

        # Modify the widget to display `category_desc`
        # self.fields['line_item_category'].widget = forms.Select(
        #     choices=[(cat.pk, cat.category_description)
        #              for cat in CategoryModel.objects.all()]
        # )
        # Set disabled fields
        # instance = kwargs.get('instance', None)
        # if instance:
        #     # Disabling certain fields
        #     # self.fields['line_item_id'].disabled = True
        #     self.fields['line_item_parent_line_item'].disabled = True

        instance = kwargs.get('instance', None)

        # Formulate the HTML strings with actual values if the instance exists
        id_html = '<p><strong>ID:</strong> {}</p>'.format(instance.line_item_id if instance else 'N/A')
        created_at_html = '<p><strong>Created At:</strong> {}</p>'.format(instance.line_item_created_at if instance else 'N/A')
        updated_at_html = '<p><strong>Last Updated At:</strong> {}</p>'.format(instance.line_item_last_updated_at if instance else 'N/A')
        parent_line_item_html = '<p><strong>Parent Line Item:</strong> {}</p>'.format(instance.line_item_parent_line_item if instance else 'N/A')
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Row(
                Column(HTML(id_html), css_class='col-6'),
                Column(HTML(updated_at_html), css_class='col-6'),
            css_class='p-1 my-1'),
            Row(
                Column(HTML(parent_line_item_html), css_class='col-6'),
                Column(HTML(created_at_html), css_class='col-6'),
            css_class='p-1 my-1'),
            Row(
                Column(Field('line_item_type',css_class='form-select'), css_class='col-3 my-1'),
                Column(Field('line_item_description',css_class='form-control'), css_class='col-8  my-1'),
            css_class='form-group p-1 my-1'),
        )