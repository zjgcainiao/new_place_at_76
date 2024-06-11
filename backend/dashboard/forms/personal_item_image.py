from .base import forms, inlineformset_factory
from homepageapp.models import PersonalItemImage, PersonalItem


class PersonalItemImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # Make this field optiona

    class Meta:
        model = PersonalItemImage
        fields = ['image', 'image_description']


PersonalItemImageInlineFormSet = inlineformset_factory(
    PersonalItem,
    PersonalItemImage,
    form=PersonalItemImageForm,
    extra=3,
)
