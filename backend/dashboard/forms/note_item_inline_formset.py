from .base import forms, FormHelper, inlineformset_factory
from .note_item_update import NoteItemUpdateForm
from homepageapp.models import LineItemsNewSQL02Model, NoteItemsNewSQL02Model




NoteItemInlineFormset = inlineformset_factory(LineItemsNewSQL02Model, NoteItemsNewSQL02Model,
                                               form=NoteItemUpdateForm,
                                               extra=0,
                                               can_delete=True,
                                               )