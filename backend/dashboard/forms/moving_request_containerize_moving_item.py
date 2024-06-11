
from .base import forms, inlineformset_factory

from homepageapp.models import MovingRequest, \
    MovingRequestContainerizeMovingItem


class MovingRequestContainerizeMovingItemForm(forms.ModelForm):

    class Meta:
        model = MovingRequestContainerizeMovingItem
        fields = ['container', 'moving_item', ]


MovingRequestContainerizeMovingItemsFormSet = inlineformset_factory(
    MovingRequest,
    MovingRequestContainerizeMovingItem,
    form=MovingRequestContainerizeMovingItemForm,
    fields=['container', 'moving_item',],
    extra=3,
    can_delete=True
)
