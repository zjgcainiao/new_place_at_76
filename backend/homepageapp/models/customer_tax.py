from .base import models, InternalUser

from .tax import TaxesModel
from .customer import CustomersNewSQL02Model

class CustomerTaxesModel(models.Model):
    tax_id = models.ForeignKey(TaxesModel, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)
    customertaxes_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    customertaxes_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customertaxes_new_03'
        ordering = ["-tax_id", '-customer_id']
        verbose_name = 'customertax'
        verbose_name_plural = 'customertaxes'
