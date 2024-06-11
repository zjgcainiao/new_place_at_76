from .base import models, InternalUser


class PaymentTransactionsModel(models.Model):
    payment_transaction_id = models.AutoField(primary_key=True)
    payment_transcation_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    payment_transcation_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='payment_transaction_tech_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='payment_transaction_modified', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'paymenttransactions_new_03'
        ordering = ["-payment_transaction_id",]
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'

