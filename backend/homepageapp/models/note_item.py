from .base import models, InternalUser
from .line_item import LineItemsNewSQL02Model


class NoteItemsNewSQL02Model(models.Model):
    note_item_id = models.AutoField(primary_key=True)
    # when it is a foreign key,"_id" is added at the end of the field name
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='lineitem_noteitem')
    note_item_text = models.TextField(null=True, blank=True)
    note_item_is_printed_on_order = models.BooleanField(default=True)
    note_item_tech_observation = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(
        InternalUser, related_name='note_item_created',
        on_delete=models.SET_NULL,
        null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser,
        related_name='note_item_modified',
        on_delete=models.SET_NULL, null=True, blank=True)
    note_item_created_at = models.DateTimeField(auto_now_add=True)
    note_item_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'noteitems_new_03'
        ordering = ["-note_item_id"]
        verbose_name = 'noteitem'
        verbose_name_plural = 'noteitems'
