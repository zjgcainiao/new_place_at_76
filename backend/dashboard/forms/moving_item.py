from .base import forms, inlineformset_factory, BaseInlineFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from homepageapp.models import MovingItem, PersonalItem, MovingRequest, MovingRequestContainerizeMovingItem


class MovingItemForm(forms.ModelForm):
    class Meta:
        model = MovingItem
        fields = ['moving_item', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up crispy form helper
        # self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.layout = Layout(
        #     Row(
        #         Column('moving_item', css_class='form-group col-md-6 mb-0'),
        #         Column('container', css_class='form-group col-md-6 mb-0'),
        #         css_class='form-row'
        #     ),
        #     Submit('submit', 'Create Moving Request',
        #            css_class='btn btn-outline-dark')
        # )
        # Ensuring only items marked as containers are shown in the container field
        # self.fields['moving_item'].queryset = PersonalItem.objects.all()
        self.fields['container'].queryset = PersonalItem.objects.filter(
            is_storage_container=True)

        # def clean(self):
        #     cleaned_data = super().clean()
        #     container = cleaned_data.get('container')
        #     if container and not container.is_storage_container:
        #         raise forms.ValidationError(
        #             "Selected container is not marked as a container. \
        #                 Check the item_type field.")
        #     return cleaned_data

# Create an inline formset for moving items inside containers


class BaseMovingItemInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        # Filter by the container provided in the instance
        queryset = super().get_queryset()
        if self.instance:
            return queryset.filter(container=self.instance)
        return queryset.none()


MovingItemInlineFormSet = inlineformset_factory(
    PersonalItem,
    MovingItem,
    form=MovingItemForm,
    formset=BaseMovingItemInlineFormSet,
    extra=4,
    fk_name='moving_item',
)
