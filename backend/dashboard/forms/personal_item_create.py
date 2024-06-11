from .personal_item_update import PersonalItemUpdateForm


class PersonalItemCreateForm(PersonalItemUpdateForm):
    class Meta(PersonalItemUpdateForm.Meta):
        # + ['any_additional_field']
        fields = PersonalItemUpdateForm.Meta.fields

    # Add any additional fields or methods specific to the create form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # child form specific code
