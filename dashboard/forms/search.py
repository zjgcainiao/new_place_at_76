
from .base import forms, FormHelper, Layout, Div, Submit
from crispy_forms.bootstrap import PrependedText
from django.utils.safestring import mark_safe
from .automan_base import AutomanBaseForm

class SearchForm(AutomanBaseForm):
    search_query = forms.CharField(label='Search', widget=forms.TextInput(
        attrs={'placeholder': 'enter a phone number, license plate to search.','type':'search'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize FormHelper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        # Form layout
        self.helper.layout = Layout(
            Div(
                # PrependedText is used to add the search icon as a prepended element to your input field
                PrependedText('search_query', mark_safe('<span class="mdi mdi-magnify search-icon"></span>'), active=True,_class='form-control dropdown-toggle'),
                Submit('submit', 'Search', css_class='btn btn-primary input-group-text'),
                css_class='form-group  p-1 m-1',
            ),
            
        )