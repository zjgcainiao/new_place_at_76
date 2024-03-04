from .base import forms, Layout, Field, FormHelper


class GeminiChatBotForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your message here. No lewd or offensive content please.'}),
        help_text='Do not enter any sensitive information, such as your address, name, ssn, banking or credit card info, etc.',
        label='Message'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # True
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('message', css_class=''),
        )
