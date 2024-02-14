from .base import forms, FormHelper, inlineformset_factory
from .part_item_update import PartItemUpdateForm
from homepageapp.models import LineItemsNewSQL02Model, PartItemModel

PartItemInlineFormset = inlineformset_factory(LineItemsNewSQL02Model, PartItemModel,
                                              form=PartItemUpdateForm, 
                                              extra=0,
                                              can_delete=True,
                                              )