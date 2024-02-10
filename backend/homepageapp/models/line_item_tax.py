from .base import models, InternalUser

from .line_item import LineItemsNewSQL02Model


class lineItemTaxesNewSQL02Model(models.Model):
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='taxes')
    line_item_tax_id = models.IntegerField(null=True)
    line_item_tax_charged = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_tax_rate = models.DecimalField(max_digits=9, decimal_places=2)
    line_item_tax_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='line_item_tax_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='line_item_tax_modified', on_delete=models.SET_NULL, null=True, blank=True)
    line_item_tax_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'lineitemtaxes_new_03'
        ordering = ["-line_item_id"]