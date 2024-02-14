from .base import inlineformset_factory
from .labor_item_update import LaborItemUpdateForm
from homepageapp.models import LineItemsNewSQL02Model, LaborItemModel

LaborItemInlineFormset = inlineformset_factory(LineItemsNewSQL02Model, LaborItemModel,
                                               form=LaborItemUpdateForm,
                                               extra=0,
                                               can_delete=True,
                                               )
