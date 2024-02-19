from .base import modelformset_factory
from homepageapp.models import LineItemsNewSQL02Model
from .line_item_update import LineItemUpdateForm


LineItemModelFormset = modelformset_factory(LineItemsNewSQL02Model, form=LineItemUpdateForm, extra=0)