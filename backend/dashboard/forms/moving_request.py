from .base import forms, FormHelper, Layout, Submit, Row, Column, \
    inlineformset_factory
from homepageapp.models import MovingRequest, \
    MovingRequestContainerizeMovingItem
from .moving_request_containerize_moving_item import \
    MovingRequestContainerizeMovingItemForm
from django.utils import timezone
from .personal_item_update import PersonalItemUpdateForm
from .moving_item import MovingItemForm


class MovingRequestForm(forms.ModelForm):
    class Meta:
        model = MovingRequest
        fields = ['moved_by', 'move_date', 'status',
                  'origin_location', 'destination_location', 'moving_notes']
        widgets = {
            'move_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'move_by': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self):
        moving_request = super().save(commit=False)
        if not self.cleaned_data['request_number']:
            # create a today date based on the timezone
            today = timezone.now().date()

            # get the last request number of the day
            last_request_number = MovingRequest.objects.filter(
                request_number__startswith=today.strftime(
                    '%Y%m%d'
                )
            ).order_by(
                '-request_number'
            ).first()
            # if there is no request number for the day, set the request number to 0001
            if not last_request_number:
                moving_request.request_number = \
                    f"{today.strftime('%Y%m%d')}-0001"
            # otherwise, increment the last request number by 1
            else:
                last_request_number = last_request_number.request_number
                new_request_number = int(
                    last_request_number[len(today.strftime('%Y%m%d')) + 1:]) + 1
                moving_request.request_number = \
                    f"{today.strftime('%Y%m%d')}-{new_request_number:04}"

        moving_request.save()
        return moving_request


# Create an inline formset for containers linked to a MovingRequest
MovingRequestInlineFormset = inlineformset_factory(
    MovingRequest,
    MovingRequestContainerizeMovingItem,
    # form=PersonalItemUpdateForm,
    form=MovingItemForm,
    fields=['moving_item', 'container'],
    extra=1,
)
