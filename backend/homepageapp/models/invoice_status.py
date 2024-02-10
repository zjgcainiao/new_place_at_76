from .base import models, InternalUser

class InvoiceStatusModel(models.Model):
    invoice_status_id = models.AutoField(primary_key=True)
    invoice_status_description = models.CharField(max_length=30, null=True)
    invoice_status_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='invoice_status_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='invoice_status_modified', on_delete=models.SET_NULL, null=True, blank=True)
    invoice_status_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'invoicestatuses_new_03'
        ordering = ["invoice_status_id"]
        verbose_name = 'invoicestatus'
        verbose_name_plural = 'invoicestatuses'
