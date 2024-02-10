from .base import models, InternalUser
from .repair_order import RepairOrdersNewSQL02Model
from .customer import CustomersNewSQL02Model
from .invoice_status import InvoiceStatusModel
from .payment_transaction import PaymentTransactionsModel
from .account_class import AccountClassModel

class PaymentsModel(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_repair_order = models.ForeignKey(
        RepairOrdersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='payment_repairorders')
    payment_record_number = models.IntegerField(null=True)
    payment_customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='payment_customers')
    payment_date = models.DateTimeField(null=True)
    payment_check_data = models.CharField(
        max_length=100, null=True, blank=True)
    payment_auth_data = models.CharField(max_length=100, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_invoice_status = models.ForeignKey(
        InvoiceStatusModel, on_delete=models.SET_NULL, null=True, related_name='payment_invoicestatuses')
    payment_is_NSF = models.BooleanField(default=False)
    payment_is_NSF_reversal = models.BooleanField(default=False)
    payment_is_fee_payment = models.BooleanField(default=False)
    payment_total_payment = models.DecimalField(
        max_digits=10, decimal_places=2)
    payment_deletion_date = models.DateTimeField(null=True)
    payment_transcation = models.ForeignKey(
        PaymentTransactionsModel, on_delete=models.SET_NULL, null=True, related_name='payment_transactions')
    payment_account_class = models.ForeignKey(
        AccountClassModel, on_delete=models.SET_NULL, null=True, related_name='payment_accountclasses')
    payment_verification_data = models.CharField(
        max_length=200, null=True, blank=True)
    payment_receipt_one = models.CharField(
        max_length=200, null=True, blank=True)
    payment_receipt_two = models.CharField(
        max_length=200, null=True, blank=True)
    payment_receipt_three = models.CharField(
        max_length=200, null=True, blank=True)

    payment_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    payment_last_updated_at = models.CharField(
        max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='payment_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='payment_modified', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'payments_new_03'
        ordering = ["-payment_id",]
        verbose_name = 'payment'
        verbose_name_plural = 'payments'